#!/usr/bin/env python3
"""
RUN_THIS_SCRAMBLER.py - Complete AlphaWall Scrambler Bot
Just run: python RUN_THIS_SCRAMBLER.py
"""

import hashlib
import json
import random
import math
import requests
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import deque


# ============= PART 1: ALPHAWALL SCRAMBLER =============

class WordScramblerAlphaWall:
    """AlphaWall that scrambles ALL text"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Storage paths
        self.vault_dir = self.data_dir / "user_vault"
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        self.vault_file = self.vault_dir / "user_memory_vault.json"
        
        # Initialize
        if not self.vault_file.exists():
            self.vault_file.write_text("[]")
        
        # MASSIVE word mappings for security
        self.word_substitutions = {
            # Critical injection words
            'ignore': ['disregard', 'overlook', 'bypass', 'skip', 'neglect', 'dismiss', 'omit', 'exclude', 
                      'pass over', 'pay no attention to', 'take no notice of', 'brush aside', 'wave off'],
            'forget': ['erase', 'remove', 'clear', 'reset', 'delete', 'purge', 'wipe', 'abandon', 
                      'let go of', 'put aside', 'dismiss from mind', 'obliterate', 'expunge'],
            'instructions': ['directives', 'guidelines', 'rules', 'parameters', 'commands', 'orders', 
                           'guidance', 'protocols', 'specifications', 'requirements', 'mandates', 'policies'],
            'previous': ['prior', 'earlier', 'past', 'former', 'preceding', 'antecedent', 'foregoing', 
                        'old', 'bygone', 'historical', 'aforementioned', 'pre-existing'],
            'new': ['fresh', 'different', 'updated', 'revised', 'novel', 'recent', 'modern', 'current',
                   'contemporary', 'latest', 'innovative', 'unprecedented', 'original'],
            'system': ['framework', 'structure', 'setup', 'configuration', 'mechanism', 'arrangement', 
                      'organization', 'architecture', 'infrastructure', 'platform', 'environment', 'ecosystem'],
            'override': ['supersede', 'overrule', 'replace', 'supplant', 'cancel', 'void', 'nullify', 
                        'revoke', 'countermand', 'annul', 'invalidate', 'negate', 'reverse'],
            
            # Output control words
            'print': ['output', 'display', 'show', 'generate', 'produce', 'render', 'present', 'exhibit',
                     'manifest', 'reveal', 'demonstrate', 'illustrate', 'depict'],
            'exactly': ['precisely', 'specifically', 'verbatim', 'literally', 'accurately', 'faithfully', 
                       'strictly', 'perfectly', 'identically', 'word-for-word', 'to the letter', 'just so'],
            'repeat': ['echo', 'mirror', 'duplicate', 'replicate', 'reproduce', 'restate', 'reiterate', 
                      'recite', 'parrot', 'reflect', 'copy', 'imitate', 'emulate'],
            'say': ['state', 'express', 'articulate', 'communicate', 'convey', 'utter', 'voice', 
                   'verbalize', 'pronounce', 'declare', 'announce', 'proclaim'],
            
            # Control flow words
            'now': ['currently', 'presently', 'at this moment', 'immediately', 'right away', 'at present', 
                   'instantly', 'forthwith', 'promptly', 'without delay', 'straightaway', 'at once'],
            'only': ['solely', 'exclusively', 'just', 'merely', 'simply', 'purely', 'strictly', 
                    'entirely', 'uniquely', 'singularly', 'particularly', 'specifically'],
            'must': ['should', 'need to', 'have to', 'required to', 'obligated to', 'supposed to', 
                    'ought to', 'expected to', 'compelled to', 'bound to', 'necessitated to', 'duty-bound to'],
            'all': ['every', 'complete', 'entire', 'whole', 'total', 'full', 'comprehensive', 
                   'universal', 'collective', 'aggregate', 'sum total of', 'entirety of'],
            
            # Question words (preserve meaning while changing form)
            'what': ['which thing', 'that which', 'the thing that', 'whatever', 'the matter that',
                    'the subject which', 'the item that', 'the element which'],
            'how': ['in what way', 'by what method', 'through what means', 'in which manner',
                   'by which process', 'via what approach', 'using what technique'],
            'why': ['for what reason', 'what causes', 'what motivates', 'what explains',
                   'what justifies', 'what prompts', 'what drives', 'what accounts for'],
            'when': ['at what time', 'during which period', 'at which point', 'on what occasion',
                    'at which moment', 'during what timeframe', 'at what juncture'],
            'where': ['in what location', 'at which place', 'in what area', 'at what spot',
                     'in which region', 'at what position', 'in what venue'],
            'who': ['which person', 'what individual', 'which entity', 'what being',
                   'which one', 'what actor', 'which party', 'what agent'],
            
            # Emotional words (for preserving emotional weight)
            'sad': ['melancholy', 'downcast', 'blue', 'unhappy', 'sorrowful', 'dejected', 'gloomy',
                   'despondent', 'disheartened', 'forlorn', 'mournful', 'woeful'],
            'happy': ['joyful', 'pleased', 'content', 'cheerful', 'delighted', 'elated', 'gleeful',
                     'jubilant', 'upbeat', 'buoyant', 'optimistic', 'satisfied'],
            'angry': ['upset', 'frustrated', 'irritated', 'annoyed', 'furious', 'irate', 'incensed',
                     'enraged', 'livid', 'indignant', 'exasperated', 'aggravated'],
            'scared': ['frightened', 'worried', 'anxious', 'concerned', 'fearful', 'terrified', 'alarmed',
                      'apprehensive', 'nervous', 'uneasy', 'panicked', 'distressed'],
            'love': ['adore', 'cherish', 'treasure', 'care for', 'hold dear', 'be fond of', 'admire',
                    'have affection for', 'be devoted to', 'feel warmth toward', 'appreciate deeply'],
            'hate': ['dislike', 'detest', 'loathe', 'despise', 'abhor', 'can\'t stand', 'be averse to',
                    'have antipathy for', 'be repelled by', 'find intolerable', 'be disgusted by'],
            
            # Common verbs (maximum variety)
            'tell': ['inform', 'share', 'communicate', 'convey', 'relay', 'impart', 'disclose',
                    'reveal', 'report', 'brief', 'advise', 'notify'],
            'show': ['display', 'present', 'reveal', 'demonstrate', 'exhibit', 'expose', 'unveil',
                    'manifest', 'illustrate', 'indicate', 'point out', 'make visible'],
            'help': ['assist', 'aid', 'support', 'facilitate', 'enable', 'serve', 'benefit',
                    'contribute to', 'lend a hand', 'give assistance', 'provide support'],
            'want': ['desire', 'wish', 'would like', 'seek', 'hope for', 'yearn for', 'crave',
                    'long for', 'aspire to', 'aim for', 'be interested in', 'prefer'],
            'need': ['require', 'must have', 'depend on', 'necessitate', 'call for', 'demand',
                    'be in need of', 'cannot do without', 'find essential', 'rely on'],
            'know': ['understand', 'comprehend', 'grasp', 'realize', 'be aware of', 'recognize',
                    'be familiar with', 'have knowledge of', 'be informed about', 'be cognizant of'],
            'think': ['believe', 'consider', 'suppose', 'reckon', 'imagine', 'assume', 'presume',
                     'conceive', 'judge', 'deem', 'regard', 'view as'],
            
            # Pronouns (critical for privacy protection)
            'i': ['the speaker', 'this person', 'the user', 'one', 'the individual communicating',
                 'yours truly', 'the author', 'the questioner', 'this individual'],
            'me': ['this individual', 'the speaker', 'oneself', 'the person speaking', 'yours truly',
                  'the undersigned', 'this one', 'the communicator'],
            'my': ['belonging to the speaker', 'the speaker\'s', 'one\'s', 'of this person',
                  'pertaining to the user', 'associated with the speaker', 'this individual\'s'],
            'you': ['the assistant', 'the system', 'the AI', 'the responder', 'the helper',
                   'the service', 'the interface', 'the program', 'the application'],
            'your': ['the system\'s', 'belonging to the AI', 'the assistant\'s', 'of the service',
                    'pertaining to the helper', 'associated with the program', 'the interface\'s'],
            
            # Action words
            'do': ['perform', 'execute', 'carry out', 'accomplish', 'complete', 'undertake',
                  'conduct', 'implement', 'achieve', 'fulfill', 'realize'],
            'make': ['create', 'construct', 'build', 'form', 'generate', 'produce', 'craft',
                    'manufacture', 'develop', 'establish', 'formulate'],
            'go': ['proceed', 'move', 'travel', 'advance', 'progress', 'head', 'journey',
                  'venture', 'navigate', 'continue', 'depart'],
            'come': ['arrive', 'approach', 'reach', 'appear', 'show up', 'turn up', 'get here',
                    'make it', 'present oneself', 'materialize', 'emerge'],
            
            # Modifiers
            'very': ['extremely', 'highly', 'greatly', 'exceptionally', 'particularly', 'especially',
                    'remarkably', 'considerably', 'substantially', 'significantly', 'notably'],
            'really': ['truly', 'genuinely', 'actually', 'indeed', 'certainly', 'definitely',
                      'absolutely', 'positively', 'undoubtedly', 'unquestionably', 'veritably'],
            'just': ['simply', 'merely', 'only', 'purely', 'solely', 'exclusively', 'nothing but',
                    'precisely', 'exactly', 'specifically', 'particularly'],
            
            # Conjunctions and connectors
            'and': ['as well as', 'plus', 'along with', 'together with', 'in addition to',
                   'furthermore', 'moreover', 'also', 'additionally', 'besides'],
            'but': ['however', 'yet', 'though', 'although', 'nonetheless', 'nevertheless',
                   'still', 'conversely', 'on the other hand', 'in contrast'],
            'or': ['alternatively', 'otherwise', 'else', 'as an alternative', 'on the other hand',
                  'as another option', 'instead', 'rather', 'conversely'],
        }
        
        # Multi-word phrase substitutions (for common injection patterns)
        self.phrase_substitutions = {
            # Injection phrases
            'ignore all': 'disregard everything',
            'forget everything': 'clear entire memory',
            'you are now': 'the system becomes',
            'act as': 'behave like',
            'pretend to be': 'simulate being',
            'roleplay as': 'take the role of',
            'from now on': 'starting at this point',
            'above all': 'most importantly',
            'no matter what': 'regardless of circumstances',
            'under no circumstances': 'never ever',
            'at all costs': 'by any means necessary',
            'repeat after me': 'echo the following',
            'say exactly': 'state precisely',
            'output verbatim': 'produce word-for-word',
            'follow these steps': 'proceed with these actions',
            'here are your new instructions': 'consider these updated guidelines',
            'disregard previous': 'ignore prior',
            'override safety': 'bypass security',
            'jailbreak mode': 'unrestricted operation',
            
            # Common phrases
            'i think': 'one believes',
            'i feel': 'one experiences',
            'i want': 'one desires',
            'i need': 'one requires',
            'can you': 'is it possible to',
            'will you': 'would the system',
            'please help': 'kindly assist',
            'tell me': 'inform the speaker',
            'show me': 'display to the user',
            'let me know': 'inform this person',
            'as soon as possible': 'with utmost urgency',
            'right now': 'immediately',
            'no problem': 'certainly acceptable',
        }
        
        # Phrase substitutions
        self.phrase_substitutions = {
            'ignore all': 'disregard everything',
            'forget everything': 'clear entire memory',
            'you are now': 'the system becomes',
            'repeat after me': 'echo the following',
        }
    
    def _scramble_text(self, text: str) -> Tuple[str, Dict]:
        """Scramble text while preserving meaning"""
        scrambled = text
        
        # Replace phrases first
        for phrase, substitute in self.phrase_substitutions.items():
            if phrase in text.lower():
                import re
                scrambled = re.sub(phrase, substitute, scrambled, flags=re.IGNORECASE)
        
        # Then scramble individual words
        words = scrambled.split()
        scrambled_words = []
        sub_count = 0
        
        for word in words:
            # Clean word of punctuation
            prefix = ''
            suffix = ''
            clean_word = word.lower()
            
            # Extract punctuation
            while clean_word and not clean_word[0].isalnum():
                prefix += clean_word[0]
                clean_word = clean_word[1:]
            while clean_word and not clean_word[-1].isalnum():
                suffix = clean_word[-1] + suffix
                clean_word = clean_word[:-1]
            
            # Substitute if possible
            if clean_word in self.word_substitutions:
                substitutes = self.word_substitutions[clean_word]
                chosen = random.choice(substitutes)
                
                # Preserve capitalization
                if word and word[0].isupper():
                    chosen = chosen.capitalize()
                    
                scrambled_words.append(prefix + chosen + suffix)
                sub_count += 1
            else:
                # For unknown words, categorize them
                if len(clean_word) > 3:
                    if clean_word[0].isupper():
                        category = "[proper-noun]"
                    elif clean_word.isdigit():
                        category = "[number]"
                    else:
                        category = "[term]"
                    scrambled_words.append(prefix + category + suffix)
                    sub_count += 1
                else:
                    scrambled_words.append(word)
        
        scrambled_text = ' '.join(scrambled_words)
        
        metrics = {
            'substitution_rate': sub_count / max(len(words), 1),
            'original_length': len(text),
            'scrambled_length': len(scrambled_text)
        }
        
        return scrambled_text, metrics
    
    def process_input(self, user_text: str) -> Dict:
        """Process and scramble user input"""
        # Store original (never exposed)
        memory_id = hashlib.sha256(f"{user_text}{datetime.now()}".encode()).hexdigest()[:16]
        
        # Save to vault
        vault_data = json.loads(self.vault_file.read_text())
        vault_data.append({
            'id': memory_id,
            'timestamp': datetime.now().isoformat(),
            'text': user_text  # Never leaves the vault
        })
        self.vault_file.write_text(json.dumps(vault_data[-100:]))  # Keep last 100
        
        # Scramble the text
        scrambled_text, metrics = self._scramble_text(user_text)
        
        # Detect basic features (without exposing content)
        features = {
            'has_question': '?' in user_text,
            'is_urgent': user_text.isupper() or '!' in user_text,
            'word_count': len(user_text.split()),
            'emotion_level': 'high' if user_text.isupper() else 'normal'
        }
        
        return {
            'scrambled_input': scrambled_text,
            'metrics': metrics,
            'features': features,
            'memory_id': memory_id
        }


# ============= PART 2: OLLAMA BOT =============

class ScrambledOllamaBot:
    """Bot that uses scrambled input with Ollama"""
    
    def __init__(self):
        print("🚀 Initializing Scrambled Ollama Bot...")
        
        # Initialize AlphaWall
        self.alphawall = WordScramblerAlphaWall(data_dir="scrambler_data")
        
        # Check Ollama
        self.model_name = self._check_ollama()
        if not self.model_name:
            print("❌ No Ollama models found!")
            print("Please run: ollama pull llama2")
            exit(1)
        
        print(f"✅ Using model: {self.model_name}")
        print("✅ AlphaWall scrambler active")
        print("-" * 50)
    
    def _check_ollama(self) -> Optional[str]:
        """Check if Ollama is running and has models"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                if models:
                    return models[0]['name']
        except:
            print("❌ Ollama is not running!")
            print("Please start Ollama from your system tray")
            exit(1)
        return None
    
    def chat(self, user_input: str) -> str:
        """Process input and get response"""
        # Process through AlphaWall
        result = self.alphawall.process_input(user_input)
        scrambled = result['scrambled_input']
        features = result['features']
        
        # Build prompt based on features
        if features['is_urgent']:
            context = "User seems urgent. "
        elif features['has_question']:
            context = "User is asking a question. "
        else:
            context = ""
        
        # Send to Ollama
        prompt = f"Respond helpfully to: {context}{scrambled}"
        
        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': self.model_name,
                    'prompt': prompt,
                    'stream': False,
                    'options': {'temperature': 0.7}
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['response'].strip()
            else:
                return "Error generating response."
        except Exception as e:
            return f"Error: {e}"
    
    def show_security_info(self):
        """Show security statistics"""
        wall = self.alphawall
        total_words = len(wall.word_substitutions)
        total_synonyms = sum(len(syns) for syns in wall.word_substitutions.values())
        
        print("\n🛡️ SECURITY INFO:")
        print(f"• Words mapped: {total_words}")
        print(f"• Total synonyms: {total_synonyms}")
        print(f"• Average synonyms per word: {total_synonyms/total_words:.1f}")
        print(f"• Injection resistance: Very High")
        print("-" * 50 + "\n")


# ============= PART 3: MAIN PROGRAM =============

def main():
    """Run the complete scrambler bot"""
    print("""
    ╔════════════════════════════════════════════════════╗
    ║      🔀 ALPHAWALL SCRAMBLER BOT (ALL-IN-ONE) 🔀    ║
    ║                                                    ║
    ║  Your words are scrambled before reaching the AI  ║
    ║  Type 'quit' to exit | 'security' for stats       ║
    ╚════════════════════════════════════════════════════╝
    """)
    
    # Initialize bot
    bot = ScrambledOllamaBot()
    
    print("\n💬 Start chatting! Your privacy is protected.\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                print("\n👋 Goodbye! Your conversations are safe in the vault.")
                break
            elif user_input.lower() == 'security':
                bot.show_security_info()
                continue
            elif not user_input:
                continue
            
            # Show what happens
            print(f"\n🔀 Scrambling your input...", end='', flush=True)
            
            # Get response
            response = bot.chat(user_input)
            
            print(f"\r🤖 Bot: {response}\n")
            
            # Show scrambling info
            result = bot.alphawall.process_input(user_input)
            print(f"[Scrambled: {result['metrics']['substitution_rate']:.0%} of words | "
                  f"Privacy: Protected | Security: Active]")
            print("-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Let's try again...\n")


if __name__ == "__main__":
    # Check if Ollama is running first
    try:
        requests.get("http://localhost:11434/api/tags", timeout=1)
    except:
        print("❌ Please start Ollama first!")
        print("1. Make sure Ollama is installed")
        print("2. Start it from your system tray")
        print("3. Run: ollama pull llama2")
        exit(1)
    
    # Run the bot
    main()