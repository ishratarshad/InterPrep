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
        
        text_col = 'title'
        if 'description' in self.df.columns:
            text_col = 'description'
        
        for algo, words in keywords.items():
            self.df[f'is_{algo}'] = self.df[text_col].fillna('').str.lower().apply(
                lambda x: any(w in x for w in words)
            )
    
    def get_problems_by_criteria(self, difficulty=None, algorithm_types=None, companies=None, limit=None):
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
        
        # Filter by companies
        if companies:
            def company_match(company_str):
                if pd.isna(company_str):
                    return False
                company_list = [c.strip().lower() for c in str(company_str).split(',')]
                return any(comp.lower() in company_list for comp in companies)
            
            df = df[df['companies'].apply(company_match)]
        
        if limit:
            df = df.head(limit)
        
        problems = []
        for _, row in df.iterrows():
            # Extract related topics for display
            topics = row.get('related_topics', '')
            if pd.notna(topics):
                topics_list = [t.strip() for t in str(topics).split(',') if t.strip()]
            else:
                topics_list = []
            
            problems.append({
                'id': row.get('id', row.name),
                'title': row.get('title', ''),
                'difficulty': row.get('difficulty', 'medium'),
                'question': row.get('description', row.get('title', '')),
                'topics': topics_list,  # Add topics to the problem dict
                'companies': row.get('companies', '')
            })
        return problems
    
    def get_statistics(self):
        return {
            'total_problems': len(self.df),
            'difficulty_distribution': self.df['difficulty'].value_counts().to_dict() if 'difficulty' in self.df.columns else {},
            'algorithm_distribution': {}
        }


    def get_fixed_problem_by_id(self, problem_identifier):
        row = None
        try:
            target_id = int(problem_identifier)
        except (ValueError, TypeError):
            return None

        if 'id' in self.df.columns:
            df_match = self.df[self.df['id'].eq(target_id)]
            if not df_match.empty:
                row = df_match.iloc[0]
                
        if row is not None:
            topics = row.get('related_topics', '')
            topics_list = [t.strip() for t in str(topics).split(',') if t.strip()] if pd.notna(topics) else []
            
            return [{
                'id': row.get('id', row.name),
                'title': row.get('title', ''),
                'difficulty': row.get('difficulty', 'medium'),
                'question': row.get('description', row.get('title', '')),
                'topics': topics_list,
                'companies': row.get('companies', '')
            }]
        return None
