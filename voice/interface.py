"""Voice interface for REX - Speech recognition and text-to-speech."""
import logging
from typing import Optional, Callable
import speech_recognition as sr
import pyttsx3
from config.settings import settings

logger = logging.getLogger(__name__)


class VoiceInterface:
    """Handles voice input and output."""
    
    def __init__(self, enabled: bool = True):
        """Initialize voice interface.
        
        Args:
            enabled: Whether voice is enabled
        """
        self.enabled = enabled and settings.REX_VOICE_ENABLED
        self.recognizer = sr.Recognizer() if self.enabled else None
        self.tts_engine = pyttsx3.init() if self.enabled else None
        
        if self.tts_engine:
            self.tts_engine.setProperty('rate', settings.REX_VOICE_RATE)
        
        logger.info(f"Voice Interface initialized (enabled={self.enabled})")
    
    async def listen(self, timeout: int = 10) -> Optional[str]:
        """Listen for voice input.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Recognized text or None
        """
        if not self.enabled or not self.recognizer:
            logger.warning("Voice interface not enabled")
            return None
        
        try:
            with sr.Microphone() as source:
                logger.info("Listening for voice input...")
                audio = self.recognizer.listen(source, timeout=timeout)
            
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Voice recognition error: {e}")
            return None
        except Exception as e:
            logger.error(f"Listening error: {e}")
            return None
    
    async def speak(self, text: str) -> bool:
        """Speak text.
        
        Args:
            text: Text to speak
            
        Returns:
            Whether speaking was successful
        """
        if not self.enabled or not self.tts_engine:
            logger.debug(f"Voice disabled, text would be: {text}")
            return False
        
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            logger.debug(f"Spoke: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Speech error: {e}")
            return False
    
    async def interactive_session(self, response_handler: Callable[[str], str]) -> None:
        """Start an interactive voice session.
        
        Args:
            response_handler: Callback to handle recognized text
        """
        if not self.enabled:
            logger.warning("Voice interface not enabled")
            return
        
        logger.info("Starting interactive voice session")
        
        while True:
            text = await self.listen()
            if not text:
                await self.speak("Sorry, I didn't catch that.")
                continue
            
            if text.lower() in ["exit", "quit", "bye"]:
                await self.speak("Goodbye!")
                break
            
            response = response_handler(text)
            await self.speak(response)
