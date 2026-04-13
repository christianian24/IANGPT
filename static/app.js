document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatContainer = document.getElementById('chat-container');
    const sendButton = document.getElementById('send-button');
    
    // Sidebar Elements
    const sidebar = document.getElementById('sidebar');
    const closeSidebarBtn = document.getElementById('close-sidebar');
    const openSidebarBtn = document.getElementById('open-sidebar');
    const newChatBtn = document.getElementById('new-chat-btn');
    const searchChatInput = document.getElementById('search-chat');
    const chatList = document.getElementById('chat-list');
    
    // Modal Elements
    const deleteModal = document.getElementById('delete-modal');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    const cancelDeleteBtn = document.getElementById('cancel-delete-btn');

    // Settings Elements
    const settingsBtn = document.getElementById('settings-btn');
    const settingsModal = document.getElementById('settings-modal');
    const closeSettingsBtn = document.getElementById('close-settings-btn');
    const settingsNavBtns = document.querySelectorAll('.settings-nav-btn');
    const settingsPanels = document.querySelectorAll('.settings-panel');
    const themeSelect = document.getElementById('theme-select');
    const deleteAllChatsBtn = document.getElementById('delete-all-chats-btn');

    // Theme Logic
    function applyTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-theme');
        } else if (theme === 'light') {
            document.body.classList.remove('dark-theme');
        } else {
            // System
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                document.body.classList.add('dark-theme');
            } else {
                document.body.classList.remove('dark-theme');
            }
        }
    }

    const savedTheme = localStorage.getItem('themePreference') || 'system';
    themeSelect.value = savedTheme;
    applyTheme(savedTheme);

    themeSelect.addEventListener('change', (e) => {
        const theme = e.target.value;
        localStorage.setItem('themePreference', theme);
        applyTheme(theme);
    });

    // Settings Modal Logic
    if (settingsBtn) {
        settingsBtn.addEventListener('click', () => {
            settingsModal.style.display = 'flex';
        });
    }

    if (closeSettingsBtn) {
        closeSettingsBtn.addEventListener('click', () => {
            settingsModal.style.display = 'none';
        });
    }

    // Navigation Tabs
    settingsNavBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            settingsNavBtns.forEach(b => b.classList.remove('active'));
            settingsPanels.forEach(p => p.style.display = 'none');
            
            btn.classList.add('active');
            document.getElementById(btn.dataset.target).style.display = 'block';
        });
    });

    // Delete All Chats
    if (deleteAllChatsBtn) {
        deleteAllChatsBtn.addEventListener('click', async () => {
            const confirmed = await showDeleteConfirm('ALL chats forever');
            if (confirmed) {
                try {
                    const res = await fetch('/api/sessions/all', { method: 'DELETE' });
                    if (res.ok) {
                        settingsModal.style.display = 'none'; // Close settings automatically
                        await createNewSession();
                    } else {
                        console.error("Failed to delete all sessions");
                    }
                } catch (err) {
                    console.error('Network error during delete all', err);
                }
            }
        });
    }

    let currentSessionId = null;

    marked.setOptions({ breaks: true, gfm: true });
    marked.use(window.markedKatex({ throwOnError: false }));

    function escapeHtml(unsafe) {
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;");
    }

    function parseReasoningToText(reasoning) {
        if (!reasoning) return null;
        if (typeof reasoning === 'string') return reasoning;
        try {
            if (Array.isArray(reasoning)) {
                return reasoning.map(r => r.text || JSON.stringify(r)).join('\\n');
            }
            return JSON.stringify(reasoning, null, 2);
        } catch {
            return String(reasoning);
        }
    }

    function showDeleteConfirm(chatTitle) {
        return new Promise((resolve) => {
            const chatNameEl = document.getElementById('delete-chat-name');
            if (chatNameEl) chatNameEl.textContent = chatTitle;

            deleteModal.style.display = 'flex';
            
            const onConfirm = () => { cleanup(); resolve(true); };
            const onCancel = () => { cleanup(); resolve(false); };
            
            confirmDeleteBtn.addEventListener('click', onConfirm);
            cancelDeleteBtn.addEventListener('click', onCancel);
            
            function cleanup() {
                deleteModal.style.display = 'none';
                confirmDeleteBtn.removeEventListener('click', onConfirm);
                cancelDeleteBtn.removeEventListener('click', onCancel);
            }
        });
    }

    function appendMessage(role, content, reasoning = null, msgId = null) {
        // Remove the initial greeter if it's still there
        const initialGreeter = document.getElementById('initial-greeter');
        if (initialGreeter) initialGreeter.remove();

        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}-message`;
        if (msgId) msgDiv.dataset.id = msgId;
        
        let innerHTML = '<div class="message-inner">';
        const reasoningText = parseReasoningToText(reasoning);
        
        const parsedContent = role === 'system' || role === 'assistant' ? marked.parse(content || '') : escapeHtml(content);
        innerHTML += `<div class="message-content ${role === 'system' || role === 'assistant' ? 'markdown-body' : ''}">${parsedContent || (reasoningText ? '' : '...')}</div>`;
        
        if (role === 'user' && msgId) {
            // Encode content to be safely passed inside onclick
            const safeContent = encodeURIComponent(content);
            innerHTML += `
                <button class="edit-btn" onclick="enterEditMode(this, '${msgId}', '${safeContent}')">
                    <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                    Edit
                </button>
            `;
        }
        
        innerHTML += `</div>`;
        msgDiv.innerHTML = innerHTML;
        chatContainer.appendChild(msgDiv);
        scrollToBottom();
    }

    window.enterEditMode = function(btn, msgId, encodedContent) {
        const content = decodeURIComponent(encodedContent);
        const messageInner = btn.closest('.message-inner');
        const oldHtml = messageInner.innerHTML;
        
        messageInner.innerHTML = `
            <div class="edit-mode-container">
                <textarea class="edit-textarea"></textarea>
                <div class="edit-actions">
                    <button class="edit-cancel-btn">Cancel</button>
                    <button class="edit-save-btn">Save & Submit</button>
                </div>
            </div>
        `;
        
        const textarea = messageInner.querySelector('textarea');
        textarea.value = content;
        textarea.focus();
        
        messageInner.querySelector('.edit-cancel-btn').addEventListener('click', () => {
            messageInner.innerHTML = oldHtml;
        });
        
        messageInner.querySelector('.edit-save-btn').addEventListener('click', async () => {
            const newContent = textarea.value.trim();
            if (!newContent) return;
            
            userInput.disabled = true;
            sendButton.disabled = true;
            
            chatContainer.innerHTML = ''; 
            appendThinking();
            
            try {
                const response = await fetch('/api/chat/edit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: currentSessionId, message_id: msgId, content: newContent })
                });

                if (response.ok) {
                    await loadSession(currentSessionId);
                } else {
                    const data = await response.json();
                    alert("Error editing: " + data.error);
                    await loadSession(currentSessionId);
                }
            } catch (e) {
                console.error(e);
                alert("Connection Error.");
                await loadSession(currentSessionId);
            } finally {
                userInput.disabled = false;
                sendButton.disabled = false;
                userInput.focus();
            }
        });
    };

    function appendThinking() {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message system-message thinking-indicator-wrapper`;
        msgDiv.id = 'thinking-indicator';
        msgDiv.innerHTML = `
            <div class="message-inner">
                <div class="message-content">
                    <div class="thinking-dots">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                </div>
            </div>
        `;
        chatContainer.appendChild(msgDiv);
        scrollToBottom();
    }

    function removeThinking() {
        const indicator = document.getElementById('thinking-indicator');
        if (indicator) indicator.remove();
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Sidebar Toggle Logic
    closeSidebarBtn.addEventListener('click', () => {
        sidebar.classList.add('collapsed');
        openSidebarBtn.style.display = 'block';
    });

    openSidebarBtn.addEventListener('click', () => {
        sidebar.classList.remove('collapsed');
        openSidebarBtn.style.display = 'none';
    });

    // Sessions Logic
    async function fetchSessions(query = '') {
        try {
            const res = await fetch(`/api/sessions?q=${encodeURIComponent(query)}`);
            const data = await res.json();
            renderSessionList(data.sessions || []);
        } catch (e) {
            console.error("Failed to fetch sessions", e);
        }
    }

    function renderSessionList(sessions) {
        chatList.innerHTML = '';
        sessions.forEach(session => {
            const li = document.createElement('li');
            li.className = `chat-item ${session.id === currentSessionId ? 'active' : ''}`;
            
            li.innerHTML = `
                <span class="chat-item-title">${escapeHtml(session.title || 'New Chat')}</span>
                <button class="delete-chat-btn" title="Delete chat">
                    <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                </button>
            `;
            li.title = session.title;
            
            li.addEventListener('click', (e) => {
                if (e.target.closest('.delete-chat-btn')) return;
                loadSession(session.id);
            });
            
            const delBtn = li.querySelector('.delete-chat-btn');
            delBtn.addEventListener('click', async (e) => {
                e.stopPropagation();
                const confirmed = await showDeleteConfirm(session.title || 'New Chat');
                if (confirmed) {
                    try {
                        const res = await fetch(`/api/sessions/${session.id}`, { method: 'DELETE' });
                        if (res.ok) {
                            if (currentSessionId === session.id) {
                                await createNewSession();
                            } else {
                                fetchSessions(searchChatInput.value);
                            }
                        }
                    } catch (err) {
                        console.error('Failed to delete session', err);
                    }
                }
            });
            
            chatList.appendChild(li);
        });
    }

    async function createNewSession(loadAfter = true) {
        try {
            const res = await fetch('/api/sessions', { method: 'POST' });
            const data = await res.json();
            currentSessionId = data.session_id;
            
            chatContainer.innerHTML = '';
            document.querySelector('.main-wrapper').classList.add('empty-chat');
            
            fetchSessions(searchChatInput.value); 
        } catch (e) {
            console.error("Failed to create session", e);
        }
    }

    async function loadSession(sessionId) {
        currentSessionId = sessionId;
        try {
            const res = await fetch(`/api/sessions/${sessionId}`);
            const data = await res.json();
            
            chatContainer.innerHTML = ''; 
            
            if (data.messages && data.messages.length > 0) {
                document.querySelector('.main-wrapper').classList.remove('empty-chat');
                data.messages.forEach(msg => {
                    const role = msg.role === 'user' ? 'user' : 'system';
                    if (role !== 'system' || (role === 'system' && msg.content !== 'You are a helpful assistant.' && !msg.content.includes('You are IAN GPT'))) {
                        appendMessage(role, msg.content, msg.reasoning, msg.id);
                    }
                });
            } else {
                document.querySelector('.main-wrapper').classList.add('empty-chat');
            }
            
            fetchSessions(searchChatInput.value); 
        } catch (e) {
            console.error("Failed to load session", e);
        }
    }

    newChatBtn.addEventListener('click', () => createNewSession());
    
    searchChatInput.addEventListener('input', (e) => {
        fetchSessions(e.target.value);
    });

    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;

        // 1. As soon as a message physically exists, force the UI to enter Active Chat mode! (0ms latency)
        document.querySelector('.main-wrapper').classList.remove('empty-chat');

        // 2. Initially append the user message instantly
        appendMessage('user', message);
        userInput.value = '';
        userInput.style.height = 'auto';
        
        userInput.disabled = true;
        sendButton.disabled = true;
        appendThinking();

        // 3. If there is no session, silently bootstrap it in the background while the UI is already rendering
        if (!currentSessionId) {
            try {
                const res = await fetch('/api/sessions', { method: 'POST' });
                const data = await res.json();
                currentSessionId = data.session_id;
                fetchSessions(searchChatInput.value);
            } catch (err) {
                console.error("Failed to bootstrap backend session", err);
            }
        }

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message, session_id: currentSessionId })
            });

            const data = await response.json();
            removeThinking();

            if (response.ok) {
                // Instead of manually appending, let's reload the session so we get all IDs correctly (so user can edit it now).
                await loadSession(currentSessionId);
            } else {
                let errorMsg = '⚠️ An issue occurred with the AI. Please try again later.';
                if (data.error && (String(data.error).includes('429') || String(data.error).includes('Rate limit'))) {
                    errorMsg = '⚠️ API Limit Exceeded. Please try again later.';
                }
                appendMessage('error', errorMsg);
                // Even though there was an API error, the user's message WAS saved! We must refresh the sidebar so it drops out of blank!
                fetchSessions();
            }

        } catch (error) {
            removeThinking();
            appendMessage('system', `❌ Connection Error: Ensure Flask server is running.`);
        } finally {
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        }
    });

    fetchSessions();
});
