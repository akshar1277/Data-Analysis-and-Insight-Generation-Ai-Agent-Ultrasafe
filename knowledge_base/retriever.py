import os

class KnowledgeBaseRetriever:
    def __init__(self, kb_dir):
        self.kb_dir = kb_dir
        self.files = [f for f in os.listdir(kb_dir) if f.endswith('.md')]

    def retrieve(self, query):
        results = []
        for file in self.files:
            with open(os.path.join(self.kb_dir, file), 'r') as f:
                content = f.read()
                if query.lower() in content.lower():
                    results.append({"file": file, "content": content})
        return results 