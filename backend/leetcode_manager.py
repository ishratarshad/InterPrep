import pandas as pd
import numpy as np

class LeetCodeManager:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        self.df.columns = self.df.columns.str.lower()
        if 'difficulty' in self.df.columns:
            self.df['difficulty'] = self.df['difficulty'].str.lower()
        self.classify_problems()
    
    def classify_problems(self):
        # Simple keyword classification
        keywords = {
            'array': ['array', 'matrix'],
            'string': ['string', 'substring'],
            'tree': ['tree', 'bst'],
            'graph': ['graph', 'edge'],
            'dynamic_programming': ['dp', 'dynamic'],
            'greedy': ['greedy'],
            'backtracking': ['backtrack'],
        }
        
        # Combine title and description for better classification
        self.df['combined_text'] = (
            self.df['title'].fillna('') + ' ' + 
            self.df['description'].fillna('')
        )
        
        for algo, words in keywords.items():
            self.df[f'is_{algo}'] = self.df['combined_text'].str.lower().apply(
                lambda x: any(w in x for w in words)
            )
    
    def get_problems_by_criteria(self, difficulty=None, algorithm_types=None, limit=None):
        df = self.df.copy()
        
        if difficulty:
            df = df[df['difficulty'].isin([d.lower() for d in difficulty])]
        
        if algorithm_types:
            mask = False
            for algo in algorithm_types:
                col = f'is_{algo}'
                if col in df.columns:
                    mask |= df[col]
            df = df[mask] if isinstance(mask, pd.Series) else df
        
        if limit:
            df = df.head(limit)
        
        problems = []
        for _, row in df.iterrows():
            problems.append({
                'id': row.get('id', row.name),
                'title': row.get('title', ''),
                'difficulty': row.get('difficulty', 'medium'),
                'question': row.get('description', row.get('title', ''))
            })
        return problems
    
    def get_statistics(self):
        return {
            'total_problems': len(self.df),
            'difficulty_distribution': self.df['difficulty'].value_counts().to_dict() if 'difficulty' in self.df.columns else {},
            'algorithm_distribution': {}
        }