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
        """
        Filter problems by difficulty, algorithm types, and companies.
        
        Args:
            difficulty: List of difficulty levels (e.g., ['easy', 'medium'])
            algorithm_types: List of algorithm types (e.g., ['array', 'string'])
            companies: List of company names (e.g., ['Google', 'Microsoft'])
            limit: Maximum number of problems to return
            
        Returns:
            List of problem dictionaries
        """
        df = self.df.copy()
        
        # Filter by difficulty
        if difficulty:
            df = df[df['difficulty'].isin([d.lower() for d in difficulty])]
        
        # Filter by algorithm types
        if algorithm_types:
            mask = False
            for algo in algorithm_types:
                col = f'is_{algo}'
                if col in df.columns:
                    mask |= df[col]
            df = df[mask] if isinstance(mask, pd.Series) else df
        
        # Filter by companies
        if companies and 'companies' in df.columns:
            company_mask = False
            for company in companies:
                company_mask |= df['companies'].fillna('').str.lower().str.contains(company.lower())
            df = df[company_mask] if isinstance(company_mask, pd.Series) else df
        
        # Apply limit
        if limit:
            df = df.head(limit)
        
        # Build problem list
        problems = []
        for _, row in df.iterrows():
            problems.append({
                'id': row.get('id', row.name),
                'title': row.get('title', ''),
                'difficulty': row.get('difficulty', 'medium'),
                'question': row.get('description', row.get('title', '')),
                'companies': row.get('companies', 'N/A'),
                'category': self._get_problem_category(row)
            })
        return problems
    
    def _get_problem_category(self, row):
        """Determine the primary category for a problem based on classification."""
        categories = []
        for col in row.index:
            if col.startswith('is_') and row[col]:
                categories.append(col.replace('is_', '').replace('_', ' ').title())
        return ', '.join(categories) if categories else 'General'
    
    def get_available_companies(self):
        """Extract unique companies from the dataset."""
        if 'companies' not in self.df.columns:
            return []
        
        all_companies = set()
        for companies_str in self.df['companies'].dropna():
            # Assuming companies are comma-separated in the CSV
            companies_list = [c.strip() for c in str(companies_str).split(',')]
            all_companies.update(companies_list)
        
        return sorted(list(all_companies))
    
    def get_statistics(self):
        """Get dataset statistics including problem counts and distributions."""
        return {
            'total_problems': len(self.df),
            'difficulty_distribution': self.df['difficulty'].value_counts().to_dict() if 'difficulty' in self.df.columns else {},
            'algorithm_distribution': {},
            'companies_available': len(self.get_available_companies())
        }
