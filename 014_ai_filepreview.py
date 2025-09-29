import threading
import queue
import time
import random
from dataclasses import dataclass
from typing import Optional

@dataclass
class FileItem:
    name: str
    size: int  # Will determine read time
    
@dataclass
class PreviewRequest:
    file: FileItem
    request_id: int

@dataclass
class PreviewResult:
    file: FileItem
    content: str
    request_id: int

class FilePreviewManager:
    def __init__(self):
        self.request_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.current_request_id = 0
        self.latest_request_id = 0
        self.worker_thread = None
        self.stop_event = threading.Event()
        
    def start(self):
        """Start the background worker thread"""
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        
    def stop(self):
        """Stop the worker thread"""
        self.stop_event.set()
        if self.worker_thread:
            self.worker_thread.join()
    
    def request_preview(self, file: FileItem):
        """Request preview for a file. Cancels previous request."""
        self.current_request_id += 1
        self.latest_request_id = self.current_request_id
        
        # Clear any pending requests
        while not self.request_queue.empty():
            try:
                self.request_queue.get_nowait()
            except queue.Empty:
                break
        
        # Add new request
        request = PreviewRequest(file, self.current_request_id)
        self.request_queue.put(request)
        print(f"[UI] Requested preview for '{file.name}' (request #{request.request_id})")
        
    def _worker(self):
        """Background worker that reads files"""
        while not self.stop_event.is_set():
            try:
                request = self.request_queue.get(timeout=0.5)
                
                # Check if this request is still relevant
                if request.request_id != self.latest_request_id:
                    print(f"[Worker] Cancelling outdated request #{request.request_id} for '{request.file.name}'")
                    self.request_queue.task_done()
                    continue
                
                print(f"[Worker] Starting to read '{request.file.name}' (request #{request.request_id})")
                
                # Simulate reading file with chunked progress checks
                read_time = request.file.size / 100  # Size determines read time
                chunks = int(read_time * 10)  # Check every 0.1 seconds
                
                for chunk in range(chunks):
                    # Check if we should cancel
                    if request.request_id != self.latest_request_id:
                        print(f"[Worker] Aborting read of '{request.file.name}' - newer request arrived")
                        self.request_queue.task_done()
                        break
                    
                    time.sleep(0.1)  # Simulate reading a chunk
                else:
                    # Read completed successfully
                    # Generate mock content
                    content = self._generate_mock_content(request.file)
                    result = PreviewResult(request.file, content, request.request_id)
                    
                    # Only send result if still relevant
                    if request.request_id == self.latest_request_id:
                        self.result_queue.put(result)
                        print(f"[Worker] Completed reading '{request.file.name}'")
                    else:
                        print(f"[Worker] Discarding result for '{request.file.name}' - outdated")
                    
                    self.request_queue.task_done()
                    
            except queue.Empty:
                continue
    
    def _generate_mock_content(self, file: FileItem) -> str:
        """Generate mock file content"""
        lines = []
        num_lines = random.randint(10, 30)
        
        for i in range(num_lines):
            line_words = random.randint(5, 15)
            words = [f"word{random.randint(1, 100)}" for _ in range(line_words)]
            lines.append(" ".join(words))
        
        return "\n".join(lines)
    
    def get_latest_result(self) -> Optional[PreviewResult]:
        """Get the latest preview result if available"""
        try:
            return self.result_queue.get_nowait()
        except queue.Empty:
            return None


class TUIFileManager:
    def __init__(self):
        self.files = [
            FileItem("quick_read.txt", 50),      # ~0.5 seconds
            FileItem("medium_file.txt", 200),    # ~2 seconds
            FileItem("large_doc.txt", 500),      # ~5 seconds
            FileItem("huge_log.txt", 1000),      # ~10 seconds
            FileItem("small.txt", 30),           # ~0.3 seconds
            FileItem("config.txt", 100),         # ~1 second
            FileItem("massive.txt", 1500),       # ~15 seconds
        ]
        self.current_index = 0
        self.preview_manager = FilePreviewManager()
        self.current_preview = None
        
    def start(self):
        """Start the file manager"""
        self.preview_manager.start()
        print("=" * 60)
        print("TUI File Manager Simulation")
        print("=" * 60)
        print("\nSimulating user navigating through files quickly...")
        print("(Notice how slow reads get cancelled when moving to next file)\n")
        
    def navigate_to(self, index: int):
        """Simulate user navigating to a file"""
        self.current_index = index
        selected_file = self.files[self.current_index]
        
        print(f"\n{'='*60}")
        print(f"[UI] User selected: '{selected_file.name}' (size: {selected_file.size}, ~{selected_file.size/100:.1f}s read)")
        print(f"{'='*60}")
        
        # Request preview
        self.preview_manager.request_preview(selected_file)
        
    def update_ui(self):
        """Check for preview results and update UI"""
        result = self.preview_manager.get_latest_result()
        if result:
            self.current_preview = result
            preview_snippet = result.content[:100].replace('\n', ' ')
            print(f"\n[UI] ✓ Preview ready for '{result.file.name}':")
            print(f"     '{preview_snippet}...'")
            
    def simulate_user_interaction(self):
        """Simulate a user quickly navigating through files"""
        navigation_sequence = [
            (0, 0.2),   # Select file 0, wait 0.2s
            (3, 0.3),   # Select file 3 (huge), wait 0.3s - won't finish reading
            (1, 0.5),   # Select file 1, wait 0.5s - won't finish reading
            (4, 1.5),   # Select file 4 (small), wait 1.5s - should complete
            (6, 0.4),   # Select file 6 (massive), wait 0.4s - won't finish
            (0, 2.0),   # Back to file 0 (quick), wait 2s - should complete
        ]
        
        for file_index, wait_time in navigation_sequence:
            self.navigate_to(file_index)
            
            # Simulate UI updating while waiting
            elapsed = 0
            step = 0.1
            while elapsed < wait_time:
                time.sleep(step)
                self.update_ui()
                elapsed += step
        
        # Final wait to see if last preview completes
        print("\n" + "="*60)
        print("[UI] Waiting for final preview to complete...")
        print("="*60)
        for _ in range(30):  # Wait up to 3 seconds
            time.sleep(0.1)
            self.update_ui()
            
        self.preview_manager.stop()
        
        print("\n" + "="*60)
        print("Simulation Complete!")
        print("="*60)


# Run the simulation
if __name__ == "__main__":
    file_manager = TUIFileManager()
    file_manager.start()
    file_manager.simulate_user_interaction()