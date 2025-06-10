from django.core.management.base import BaseCommand
from chat.nlp import Chat

class Command(BaseCommand):
    help = 'Test the chat functionality'

    def handle(self, *args, **options):
        """Handle the command execution."""
        self.stdout.write(self.style.SUCCESS('Starting chat session. Type "exit" to quit.'))
        
        try:
            chat = Chat()
            self.stdout.write(self.style.SUCCESS('Chat initialized. Start typing your messages:'))
            
            while True:
                user_input = input('You: ').strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    self.stdout.write(self.style.SUCCESS('Goodbye!'))
                    break
                    
                if not user_input:
                    continue
                    
                try:
                    response = chat.answer(user_input)
                    self.stdout.write(f'Bot: {response}')
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))
                    
        except KeyboardInterrupt:
            self.stdout.write('\nChat session ended by user.')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {str(e)}'))
