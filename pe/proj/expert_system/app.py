import json
import sys
from pathlib import Path


class BookRecommenderExpertSystem:
    """
    Forward chaining expert system for book recommendations.
    Loads rules from JSON and matches user preferences to recommend books.
    """
    
    def __init__(self, rules_file='rules.json'):
        """Initialize the expert system by loading rules from JSON file."""
        self.rules_file = rules_file
        self.rules = []
        self.preferences = []
        self.user_facts = {}  # Stores user's yes/no answers
        self.load_rules()
    
    def load_rules(self):
        """Load rules and preferences from the JSON file."""
        try:
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.rules = data.get('rules', [])
                self.preferences = data.get('preferences', [])
            print(f"✓ Loaded {len(self.rules)} rules from {self.rules_file}")
        except FileNotFoundError:
            print(f"ERROR: {self.rules_file} not found!")
            print("Please create the rules.json file in the same directory.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in {self.rules_file}: {e}")
            sys.exit(1)
    
    def collect_user_preferences_cli(self):
        """Ask user yes/no questions about their reading preferences (CLI mode)."""
        print("\n" + "="*60)
        print("BOOK RECOMMENDATION SYSTEM")
        print("="*60)
        print("Please answer the following questions with 'yes' or 'no':\n")
        
        # Loop through all preferences and ask user
        for pref in self.preferences:
            while True:
                answer = input(f"Do you like {pref}? (yes/no): ").strip().lower()
                if answer in ['yes', 'y']:
                    self.user_facts[pref] = True
                    break
                elif answer in ['no', 'n']:
                    self.user_facts[pref] = False
                    break
                else:
                    print("Please answer 'yes' or 'no'.")
        
        print("\n" + "-"*60)
    
    def set_user_preferences(self, preferences_dict):
        """Set user preferences directly (useful for GUI mode)."""
        self.user_facts = preferences_dict.copy()
    
    def forward_chain(self):
        """
        Apply forward chaining algorithm to match rules with user facts.
        Returns a list of matching recommendations with explanations.
        """
        recommendations = []
        
        # Iterate through each rule
        for rule in self.rules:
            rule_id = rule.get('id', 'unknown')
            conditions = rule.get('conditions', {})
            recommendation = rule.get('recommendation', {})
            
            # Check if ALL conditions in the rule match user's facts
            all_conditions_met = True
            matched_conditions = []
            
            for condition_key, condition_value in conditions.items():
                # Get user's answer for this condition (default to False if not answered)
                user_value = self.user_facts.get(condition_key, False)
                
                if user_value == condition_value:
                    matched_conditions.append(f"{condition_key}: {condition_value}")
                else:
                    all_conditions_met = False
                    break  # No need to check further if one condition fails
            
            # If all conditions are satisfied, add this recommendation
            if all_conditions_met and matched_conditions:
                recommendations.append({
                    'rule_id': rule_id,
                    'book': recommendation,
                    'matched_conditions': matched_conditions
                })
        
        return recommendations
    
    def display_recommendations_cli(self, recommendations):
        """Display recommendations in CLI format with explanations."""
        print("\n" + "="*60)
        print("RECOMMENDATIONS")
        print("="*60)
        
        if not recommendations:
            print("\n❌ No recommendations found based on your preferences.")
            print("Try different preference combinations!")
        else:
            print(f"\n✓ Found {len(recommendations)} book(s) for you:\n")
            
            for idx, rec in enumerate(recommendations, 1):
                book = rec['book']
                print(f"{idx}. {book['title']}")
                print(f"   Author: {book['author']}")
                print(f"   Year: {book['year']}")
                print(f"   Description: {book['description']}")
                print(f"\n   WHY THIS RECOMMENDATION?")
                print(f"   Matched conditions:")
                for condition in rec['matched_conditions']:
                    print(f"   ✓ {condition}")
                print()
        
        print("="*60)
    
    def run_cli(self):
        """Run the expert system in CLI mode."""
        self.collect_user_preferences_cli()
        recommendations = self.forward_chain()
        self.display_recommendations_cli(recommendations)


class BookRecommenderGUI:
    """Tkinter-based GUI for the book recommender system."""
    
    def __init__(self):
        """Initialize the GUI application."""
        try:
            import tkinter as tk
            from tkinter import ttk, messagebox, scrolledtext
            self.tk = tk
            self.ttk = ttk
            self.messagebox = messagebox
            self.scrolledtext = scrolledtext
        except ImportError:
            print("ERROR: tkinter not available. Please run in CLI mode.")
            sys.exit(1)
        
        # Initialize expert system
        self.expert_system = BookRecommenderExpertSystem()
        
        # Create main window
        self.root = self.tk.Tk()
        self.root.title("Library Book Recommender - Expert System")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Dictionary to store checkbox variables
        self.checkbox_vars = {}
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Title
        title_frame = self.ttk.Frame(self.root, padding="10")
        title_frame.pack(fill='x')
        
        title_label = self.ttk.Label(
            title_frame,
            text="📚 Library Book Recommender",
            font=('Arial', 18, 'bold')
        )
        title_label.pack()
        
        subtitle_label = self.ttk.Label(
            title_frame,
            text="Select your reading preferences below",
            font=('Arial', 10)
        )
        subtitle_label.pack()
        
        # Preferences frame with scrollbar
        pref_frame = self.ttk.LabelFrame(
            self.root,
            text="Your Reading Preferences",
            padding="10"
        )
        pref_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create canvas and scrollbar for preferences
        canvas = self.tk.Canvas(pref_frame)
        scrollbar = self.ttk.Scrollbar(pref_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = self.ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create checkboxes for each preference
        for idx, pref in enumerate(self.expert_system.preferences):
            var = self.tk.BooleanVar()
            self.checkbox_vars[pref] = var
            
            cb = self.ttk.Checkbutton(
                scrollable_frame,
                text=pref.replace('_', ' ').title(),
                variable=var
            )
            cb.grid(row=idx, column=0, sticky='w', padx=5, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons frame
        button_frame = self.ttk.Frame(self.root, padding="10")
        button_frame.pack(fill='x')
        
        get_rec_btn = self.ttk.Button(
            button_frame,
            text="Get Recommendations",
            command=self.get_recommendations
        )
        get_rec_btn.pack(side='left', padx=5)
        
        clear_btn = self.ttk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_selections
        )
        clear_btn.pack(side='left', padx=5)
        
        exit_btn = self.ttk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit
        )
        exit_btn.pack(side='right', padx=5)
        
        # Results frame
        results_frame = self.ttk.LabelFrame(
            self.root,
            text="Recommendations",
            padding="10"
        )
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.results_text = self.scrolledtext.ScrolledText(
            results_frame,
            wrap=self.tk.WORD,
            width=70,
            height=15,
            font=('Courier', 10)
        )
        self.results_text.pack(fill='both', expand=True)
    
    def clear_selections(self):
        """Clear all checkbox selections."""
        for var in self.checkbox_vars.values():
            var.set(False)
        self.results_text.delete(1.0, self.tk.END)
    
    def get_recommendations(self):
        """Get recommendations based on selected preferences."""
        # Clear previous results
        self.results_text.delete(1.0, self.tk.END)
        
        # Collect user preferences from checkboxes
        user_prefs = {
            pref: var.get()
            for pref, var in self.checkbox_vars.items()
        }
        
        # Set preferences in expert system
        self.expert_system.set_user_preferences(user_prefs)
        
        # Run forward chaining
        recommendations = self.expert_system.forward_chain()
        
        # Display results
        if not recommendations:
            self.results_text.insert(
                self.tk.END,
                "❌ No recommendations found based on your preferences.\n"
                "Try selecting different combinations!"
            )
        else:
            self.results_text.insert(
                self.tk.END,
                f"✓ Found {len(recommendations)} book(s) for you:\n\n"
            )
            
            for idx, rec in enumerate(recommendations, 1):
                book = rec['book']
                self.results_text.insert(
                    self.tk.END,
                    f"{'='*70}\n"
                )
                self.results_text.insert(
                    self.tk.END,
                    f"{idx}. {book['title']}\n"
                )
                self.results_text.insert(
                    self.tk.END,
                    f"   Author: {book['author']}\n"
                )
                self.results_text.insert(
                    self.tk.END,
                    f"   Year: {book['year']}\n"
                )
                self.results_text.insert(
                    self.tk.END,
                    f"   Description: {book['description']}\n\n"
                )
                self.results_text.insert(
                    self.tk.END,
                    f"   WHY THIS RECOMMENDATION?\n"
                )
                self.results_text.insert(
                    self.tk.END,
                    f"   Matched conditions:\n"
                )
                for condition in rec['matched_conditions']:
                    self.results_text.insert(
                        self.tk.END,
                        f"   ✓ {condition}\n"
                    )
                self.results_text.insert(self.tk.END, "\n")
    
    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()


def main():
    """Main entry point for the application."""
    # Check if GUI mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == '--gui':
        # Run GUI mode
        app = BookRecommenderGUI()
        app.run()
    else:
        # Run CLI mode
        expert_system = BookRecommenderExpertSystem()
        expert_system.run_cli()


if __name__ == '__main__':
    main()