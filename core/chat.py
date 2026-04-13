from abc import ABC, abstractmethod
from typing import List, Dict, Any
from core.client import get_client
from config.settings import MODEL_NAME, SYSTEM_PROMPT
from core.database import get_messages, save_message, update_session_title

class BaseChatSession(ABC):
    """Abstract Base Class defining the contract for Chat Sessions (Encapsulation)"""
    def __init__(self, session_id: str = None):
        self.client = get_client()
        self.messages: List[Dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.model = MODEL_NAME
        self.session_id = session_id
        
        if self.session_id:
            # Rehydrate messages from DB
            db_messages = get_messages(self.session_id)
            for msg in db_messages:
                m = {"role": msg['role'], "content": msg['content'] or ""}
                if msg.get('reasoning'):
                     m["reasoning_details"] = msg['reasoning']
                self.messages.append(m)

    def _generate_title_if_needed(self, content: str):
        if self.session_id and len(self.messages) == 2:
            try:
                # Ask the model to analyze the text and generate a concise title!
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": f"Analyze the following message and reply with a very short 2-5 word title summarizing its topic. Never use prefixes, context, or quotes. Message: {content}"}
                    ]
                )
                title = response.choices[0].message.content.strip().strip('"').strip("'")
                if not title:
                    title = content[:30] + "..." if len(content) > 30 else content
            except Exception:
                # Fallback
                title = content[:30] + "..." if len(content) > 30 else content
                
            update_session_title(self.session_id, title)

    @abstractmethod
    def send_message(self, content: str) -> Any:
        pass

    @abstractmethod
    def regenerate_response(self) -> Any:
        pass


class StandardChatSession(BaseChatSession):
    """Child class tailored for standard non-reasoning models."""
    def send_message(self, content: str) -> Any:
        self.messages.append({"role": "user", "content": content})
        if self.session_id:
            save_message(self.session_id, "user", content)
            self._generate_title_if_needed(content)
            
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        
        assistant_message = response.choices[0].message
        self.messages.append({
            "role": "assistant",
            "content": assistant_message.content or ""
        })
        
        if self.session_id:
            save_message(self.session_id, "assistant", assistant_message.content or "")
            
        return assistant_message

    def regenerate_response(self) -> Any:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        
        assistant_message = response.choices[0].message
        self.messages.append({
            "role": "assistant",
            "content": assistant_message.content or ""
        })
        
        if self.session_id:
            save_message(self.session_id, "assistant", assistant_message.content or "")
            
        return assistant_message


class ReasoningChatSession(BaseChatSession):
    """Child class specialized for models returning reasoning traces."""
    def send_message(self, content: str) -> Any:
        self.messages.append({"role": "user", "content": content})
        if self.session_id:
            save_message(self.session_id, "user", content)
            self._generate_title_if_needed(content)
            
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            extra_body={"reasoning": {"enabled": True}}
        )
        
        assistant_message = response.choices[0].message

        # Preserve the assistant message internally
        message_to_save = {
            "role": "assistant",
            "content": assistant_message.content or "",
        }
        
        # Dynamically preserve reasoning details
        reasoning_details = getattr(assistant_message, "reasoning_details", None)
        if not reasoning_details:
             reasoning_details = getattr(assistant_message, "reasoning", getattr(assistant_message, "thought", ""))

        if reasoning_details:
             message_to_save["reasoning_details"] = reasoning_details
             
        self.messages.append(message_to_save)
        
        if self.session_id:
            save_message(self.session_id, "assistant", message_to_save["content"], str(reasoning_details) if reasoning_details else None)
            
        return assistant_message

    def regenerate_response(self) -> Any:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            extra_body={"reasoning": {"enabled": True}}
        )
        
        assistant_message = response.choices[0].message

        message_to_save = {
            "role": "assistant",
            "content": assistant_message.content or "",
        }
        
        reasoning_details = getattr(assistant_message, "reasoning_details", None)
        if not reasoning_details:
             reasoning_details = getattr(assistant_message, "reasoning", getattr(assistant_message, "thought", ""))

        if reasoning_details:
             message_to_save["reasoning_details"] = reasoning_details
             
        self.messages.append(message_to_save)
        
        if self.session_id:
            save_message(self.session_id, "assistant", message_to_save["content"], str(reasoning_details) if reasoning_details else None)
            
        return assistant_message