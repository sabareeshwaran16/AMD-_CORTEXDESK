import sys
import time
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.workspace_assistant import WorkspaceAssistant

def main():
    assistant = WorkspaceAssistant(data_dir="data")
    assistant.start()
    
    print("\n" + "="*60)
    print("LOCAL AI WORKSPACE ASSISTANT")
    print("100% Offline | Privacy-First | No Cloud Calls")
    print("="*60)
    
    try:
        while True:
            print("\nCommands:")
            print("  1. Process file")
            print("  2. Search documents")
            print("  3. View tasks")
            print("  4. View agent status")
            print("  5. Exit")
            
            choice = input("\nEnter choice: ").strip()
            
            if choice == "1":
                file_path = input("Enter file path: ").strip()
                assistant.process_file(file_path)
                print("Processing file...")
                time.sleep(2)
                
            elif choice == "2":
                query = input("Enter search query: ").strip()
                assistant.search(query)
                print("Searching...")
                time.sleep(1)
                
            elif choice == "3":
                tasks = assistant.get_tasks()
                print(f"\nFound {len(tasks)} tasks:")
                for i, task in enumerate(tasks, 1):
                    print(f"\n{i}. {task['task']}")
                    print(f"   Assignee: {task.get('assignee', 'N/A')}")
                    print(f"   Priority: {task.get('priority', 'N/A')}")
                    print(f"   Deadline: {task.get('deadline', 'N/A')}")
                
            elif choice == "4":
                status = assistant.get_status()
                print("\nAgent Status:")
                for agent_id, agent_status in status.items():
                    print(f"  {agent_id}: {agent_status}")
                
            elif choice == "5":
                break
            
            else:
                print("Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    
    finally:
        assistant.stop()
        print("Goodbye!")

if __name__ == "__main__":
    main()
