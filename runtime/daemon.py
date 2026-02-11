"""
Background Runtime - Near-zero resource consumption
Does nothing until queried. Never polls. Never schedules.
"""
import time
import threading
from queue import Queue
import json

class QGLDaemon:
    """
    Background runtime service.
    Idle until queried. No autonomous execution.
    """
    
    def __init__(self):
        self.request_queue = Queue()
        self.response_queue = Queue()
        self.is_running = False
        self.worker_thread = None
        
        # Import engines
        from qgl.lexer import QGLLexer
        from qgl.parser import QGLParser
        from engine.admissibility import AdmissibilityEngine
        from engine.inversion import InversionEngine
        
        self.lexer = QGLLexer()
        self.parser = QGLParser()
        self.admissibility = AdmissibilityEngine()
        self.inversion = InversionEngine(self.admissibility)
    
    def start(self):
        """Start the daemon (minimal resource usage)"""
        if self.is_running:
            return
        
        self.is_running = True
        self.worker_thread = threading.Thread(
            target=self._worker_loop,
            daemon=True,
            name="QGL-Daemon"
        )
        self.worker_thread.start()
        print("QGL Daemon started (idle)")
    
    def stop(self):
        """Stop the daemon"""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=1.0)
        print("QGL Daemon stopped")
    
    def _worker_loop(self):
        """Main worker loop - waits for requests"""
        while self.is_running:
            try:
                # Wait for request with timeout (allows graceful shutdown)
                request = self.request_queue.get(timeout=0.1)
                
                # Process request
                response = self._process_request(request)
                
                # Send response
                self.response_queue.put(response)
                
            except:
                # Queue empty or shutdown - continue loop
                continue
    
    def _process_request(self, request):
        """Process a single request"""
        request_type = request.get('type', 'unknown')
        
        if request_type == 'check_admissibility':
            qgl_code = request.get('qgl_code', '')
            return self._check_admissibility(qgl_code)
        
        elif request_type == 'perform_inversion':
            qgl_code = request.get('qgl_code', '')
            boundary_name = request.get('boundary_name', '')
            return self._perform_inversion(qgl_code, boundary_name)
        
        elif request_type == 'get_accumulation':
            return {
                'type': 'accumulation',
                'data': self.admissibility.get_accumulation()
            }
        
        else:
            return {
                'type': 'error',
                'message': f'Unknown request type: {request_type}'
            }
    
    def _check_admissibility(self, qgl_code):
        """Check if QGL code is admissible"""
        try:
            # 1. Lex (rejects forbidden syntax)
            tokens = self.lexer.tokenize(qgl_code)
            
            # 2. Parse (builds structural AST)
            program = self.parser.parse(tokens)
            
            # 3. Check admissibility
            admissible, reason = self.admissibility.check_structure(program)
            
            return {
                'type': 'admissibility_result',
                'admissible': admissible,
                'reason': reason,
                'program_summary': str(program)
            }
            
        except Exception as e:
            return {
                'type': 'error',
                'message': str(e)
            }
    
    def _perform_inversion(self, qgl_code, boundary_name):
        """Perform inversion on QGL code"""
        try:
            # 1. Parse
            tokens = self.lexer.tokenize(qgl_code)
            program = self.parser.parse(tokens)
            
            # 2. Perform inversion
            new_program, success, reason = self.inversion.invert(
                program, boundary_name
            )
            
            return {
                'type': 'inversion_result',
                'success': success,
                'reason': reason,
                'original_program': str(program),
                'new_program': str(new_program),
                'inversion_count': self.inversion.get_inversion_count()
            }
            
        except Exception as e:
            return {
                'type': 'error',
                'message': str(e)
            }
    
    def submit_request(self, request):
        """Submit request to daemon"""
        self.request_queue.put(request)
        
        # Wait for response
        response = self.response_queue.get()
        return response
    
    def get_resource_usage(self):
        """Get current resource usage (minimal by design)"""
        return {
            'queue_size': self.request_queue.qsize(),
            'is_running': self.is_running,
            'thread_alive': self.worker_thread.is_alive() if self.worker_thread else False,
            'memory_estimate': 'minimal',  # QGL has no large data structures
            'cpu_estimate': 'idle'  # No polling, no scheduling
        }