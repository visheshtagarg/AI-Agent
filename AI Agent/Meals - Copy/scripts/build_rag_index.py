import argparse
import os
import csv
from agents.rag_retriever_agent import RAGRetrieverAgent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--out', required=False, default='chromadb_store')
    args = parser.parse_args()

    rag = RAGRetrieverAgent(persist_dir=args.out)
    if getattr(rag, 'dependency_missing', False):
        print('Missing dependencies. Install: pip install sentence-transformers chromadb')
        return
    if not getattr(rag, 'available', False):
        print('RAG client unavailable. Check permissions on persist dir.')
        return

    docs = []
    # Simple CSV ingest (expects columns: id,text,calories,protein_g,carbs_g,fat_g)
    if os.path.isfile(args.source) and args.source.endswith('.csv'):
        with open(args.source, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                docs.append({
                    'id': row.get('id') or row.get('name') or row.get('text')[:32],
                    'text': row.get('text') or row.get('name') or '',
                    'metadata': {
                        'calories': row.get('calories'),
                        'protein_g': row.get('protein_g'),
                        'carbs_g': row.get('carbs_g'),
                        'fat_g': row.get('fat_g')
                    }
                })
    else:
        print('Only CSV ingest demo implemented.')

    if docs:
        rag.add_documents(docs)
        print(f'Indexed {len(docs)} docs into {args.out}')


if __name__ == '__main__':
    main()

