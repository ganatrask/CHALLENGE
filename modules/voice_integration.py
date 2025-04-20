import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import threading
import queue
import time

class VoiceInteractionModule:
    def __init__(self):
        """Initialize the voice interaction module."""
        self.recognizer = sr.Recognizer()
        self.speech_queue = queue.Queue()
        self.is_listening = False
        self.speech_thread = None
        
        # Initialize pygame for audio playback
        pygame.mixer.init()
        
        # Agent voice characteristics - can be customized
        self.agent_voices = {
            "agent_1": {"lang": "en", "slow": False, "voice_name": "en-US-Wavenet-B"},
            "agent_2": {"lang": "en", "slow": False, "voice_name": "en-US-Wavenet-C"},
            "agent_3": {"lang": "en", "slow": False, "voice_name": "en-US-Wavenet-D"},
            "agent_4": {"lang": "en", "slow": False, "voice_name": "en-US-Wavenet-E"}
        }
    
    def start_listening(self, callback_function):
        """
        Start listening for voice input in a separate thread.
        The callback_function will be called with the recognized text.
        """
        if self.is_listening:
            return False
            
        self.is_listening = True
        self.speech_thread = threading.Thread(target=self._listen_thread, args=(callback_function,))
        self.speech_thread.daemon = True
        self.speech_thread.start()
        return True
    
    def stop_listening(self):
        """Stop the voice recognition thread."""
        self.is_listening = False
        if self.speech_thread:
            self.speech_thread.join(timeout=1)
            self.speech_thread = None
        return True
    
    def _listen_thread(self, callback_function):
        """Background thread for continuous speech recognition."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    text = self.recognizer.recognize_google(audio)
                    if text:
                        callback_function(text)
                except sr.WaitTimeoutError:
                    pass  # No speech detected, continue listening
                except sr.UnknownValueError:
                    pass  # Speech was unintelligible
                except sr.RequestError as e:
                    print(f"Speech recognition service error: {e}")
                except Exception as e:
                    print(f"Error in speech recognition: {e}")
    
    def speak_text(self, text, agent_id=None):
        """
        Convert text to speech and play it.
        If agent_id is provided, use the corresponding voice settings.
        """
        voice_settings = self.agent_voices.get(agent_id, {"lang": "en", "slow": False})
        
        try:
            # Generate speech
            tts = gTTS(text=text, lang=voice_settings["lang"], slow=voice_settings["slow"])
            
            # Save to temporary file
            temp_file = f"temp_speech_{int(time.time())}.mp3"
            tts.save(temp_file)
            
            # Play the audio
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Clean up the temporary file
            os.remove(temp_file)
            
            return True
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            return False
    
    def queue_speech(self, text, agent_id=None):
        """Add text to the speech queue to be spoken."""
        self.speech_queue.put((text, agent_id))
        
        # If not already processing the queue, start a new thread
        if not hasattr(self, 'queue_thread') or not self.queue_thread.is_alive():
            self.queue_thread = threading.Thread(target=self._process_speech_queue)
            self.queue_thread.daemon = True
            self.queue_thread.start()
    
    def _process_speech_queue(self):
        """Process the speech queue in the background."""
        while not self.speech_queue.empty():
            text, agent_id = self.speech_queue.get()
            self.speak_text(text, agent_id)
            self.speech_queue.task_done()

# Alternative implementation using web-based speech APIs
# For a web application deployment
class WebVoiceInteractionModule:
    def __init__(self):
        """Initialize the web-based voice interaction module."""
        # This would use browser APIs in a real implementation
        pass
    
    def initialize_web_speech(self):
        """
        JavaScript to initialize browser speech recognition and synthesis.
        This would be injected into the web page.
        """
        return """
        <script>
        // Speech recognition setup
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        // Speech synthesis setup
        const synth = window.speechSynthesis;
        
        // Agent voices (will be populated when available)
        let agentVoices = {};
        
        // Initialize voices when available
        function initVoices() {
            const voices = synth.getVoices();
            if (voices.length === 0) {
                // Try again when voices are loaded
                window.speechSynthesis.onvoiceschanged = initVoices;
                return;
            }
            
            // Assign different voices to agents
            agentVoices = {
                agent_1: voices.find(voice => voice.name.includes('Male')) || voices[0],
                agent_2: voices.find(voice => voice.name.includes('Female')) || voices[1],
                agent_3: voices.find(voice => voice.name.includes('Male') && !voice.name.includes(agentVoices.agent_1.name)) || voices[2],
                agent_4: voices.find(voice => voice.name.includes('Female') && !voice.name.includes(agentVoices.agent_2.name)) || voices[3]
            };
        }
        
        // Initialize voices
        initVoices();
        
        // Start speech recognition
        function startListening(callbackFunction) {
            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                callbackFunction(transcript);
            };
            
            recognition.start();
        }
        
        // Stop speech recognition
        function stopListening() {
            recognition.stop();
        }
        
        // Text to speech
        function speakText(text, agentId = null) {
            const utterance = new SpeechSynthesisUtterance(text);
            
            if (agentId && agentVoices[agentId]) {
                utterance.voice = agentVoices[agentId];
            }
            
            synth.speak(utterance);
        }
        
        // Queue for multiple speech outputs
        const speechQueue = [];
        let isSpeaking = false;
        
        function queueSpeech(text, agentId = null) {
            speechQueue.push({ text, agentId });
            if (!isSpeaking) {
                processSpeechQueue();
            }
        }
        
        function processSpeechQueue() {
            if (speechQueue.length === 0) {
                isSpeaking = false;
                return;
            }
            
            isSpeaking = true;
            const { text, agentId } = speechQueue.shift();
            
            const utterance = new SpeechSynthesisUtterance(text);
            if (agentId && agentVoices[agentId]) {
                utterance.voice = agentVoices[agentId];
            }
            
            utterance.onend = function() {
                processSpeechQueue();
            };
            
            synth.speak(utterance);
        }
        </script>
        """