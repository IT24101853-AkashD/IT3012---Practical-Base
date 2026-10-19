# logic_engine.py

class KnowledgeBase:
    """
    Declarative Knowledge Base storing facts and Horn Clause rules
    with a Forward Chaining inference engine.
    """
    def __init__(self):
        # Attributes
        self.facts = set()   # To store unique string facts (e.g., "TargetVisible")
        self.rules = []      # To store rules as Tuples: ( [list_of_premises], "conclusion_string" )

    def tell_fact(self, fact_string):
        """Adds a fact string to the facts set."""
        self.facts.add(fact_string)

    def tell_rule(self, premise_list, conclusion_string):
        """Appends a rule as (premise_list, conclusion_string) tuple."""
        self.rules.append((premise_list, conclusion_string))

    def clear_facts(self):
        """Empties the facts set."""
        self.facts.clear()

    def forward_chain(self):
        """
        Data-driven Forward Chaining algorithm.
        Iteratively applies Modus Ponens to Horn Clauses until a fixed point is reached.
        """
        new_facts_added = True
        
        while new_facts_added:
            new_facts_added = False
            
            for premises, conclusion in self.rules:
                if conclusion not in self.facts:
                    # Modus Ponens Check: If all premises are satisfied by known facts
                    if all(p in self.facts for p in premises):
                        self.facts.add(conclusion)
                        new_facts_added = True
