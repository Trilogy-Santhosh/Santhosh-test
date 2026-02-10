#!/usr/bin/env python3
"""Command-line interface for GDriveQA."""
import sys
from pathlib import Path
from config import Config
from indexer import DocumentIndexer
from query_engine import QueryEngine


def print_banner():
    """Print application banner."""
    print("\n" + "="*70)
    print(" "*20 + "GOOGLE DRIVE Q&A SYSTEM")
    print("="*70 + "\n")


def main():
    """Main CLI entry point."""
    # Setup
    Config.setup_directories()
    
    # Validate configuration
    errors = Config.validate()
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease check your .env file and credentials.")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'index':
        # Index documents
        print_banner()
        indexer = DocumentIndexer()
        indexer.sync_and_index()
    
    elif command == 'query' or command == 'ask':
        # Query documents
        if len(sys.argv) < 3:
            print("Usage: python cli.py query \"Your question here\"")
            sys.exit(1)
        
        question = sys.argv[2]
        
        print_banner()
        print(f"Question: {question}\n")
        print("-" * 70 + "\n")
        
        engine = QueryEngine()
        result = engine.ask(question)
        
        if result['success']:
            print("Answer:")
            print(result['answer'])
            print("\n" + "-" * 70)
            print(f"\nSources used ({result['num_sources']} documents):")
            for i, source in enumerate(set(result['sources']), 1):
                print(f"  {i}. {source}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
        
        print("\n" + "="*70 + "\n")
    
    elif command == 'stats':
        # Show statistics
        print_banner()
        engine = QueryEngine()
        stats = engine.get_stats()
        
        print("Vector Store Statistics:")
        print(f"  Total documents indexed: {stats['total_files']}")
        print(f"  Total chunks: {stats['total_chunks']}")
        print(f"  Collection: {stats['collection_name']}")
        print()
    
    elif command == 'clear':
        # Clear index
        response = input("Are you sure you want to clear the entire index? (yes/no): ")
        if response.lower() == 'yes':
            indexer = DocumentIndexer()
            indexer.clear_index()
            print("Index cleared successfully.")
        else:
            print("Operation cancelled.")
    
    elif command == 'interactive':
        # Interactive mode
        print_banner()
        engine = QueryEngine()
        stats = engine.get_stats()
        
        print(f"Indexed documents: {stats['total_files']}")
        print(f"Total chunks: {stats['total_chunks']}")
        print("\nEnter your questions (type 'exit' to quit, 'stats' for statistics)\n")
        
        while True:
            try:
                question = input("\n\033[1;36mYou:\033[0m ")
                
                if question.lower() in ['exit', 'quit', 'q']:
                    print("\nGoodbye!")
                    break
                
                if question.lower() == 'stats':
                    stats = engine.get_stats()
                    print(f"\n  Documents: {stats['total_files']}")
                    print(f"  Chunks: {stats['total_chunks']}")
                    continue
                
                if not question.strip():
                    continue
                
                print("\n\033[1;32mAssistant:\033[0m ", end="")
                result = engine.ask(question)
                
                if result['success']:
                    print(result['answer'])
                    print(f"\n  \033[0;90m[Sources: {', '.join(set(result['sources'][:3]))}]\033[0m")
                else:
                    print(result.get('error', 'Could not generate answer'))
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
    
    else:
        print_usage()
        sys.exit(1)


def print_usage():
    """Print usage information."""
    print("\nGDriveQA - Query your Google Drive documents using AI")
    print("\nUsage:")
    print("  python cli.py index                  - Index all Google Drive documents")
    print("  python cli.py query \"question\"       - Ask a question")
    print("  python cli.py interactive            - Interactive Q&A mode")
    print("  python cli.py stats                  - Show index statistics")
    print("  python cli.py clear                  - Clear the index")
    print("\nExamples:")
    print("  python cli.py index")
    print("  python cli.py query \"What is the project timeline?\"")
    print("  python cli.py interactive")
    print()


if __name__ == '__main__':
    main()
