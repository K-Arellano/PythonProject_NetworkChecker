import tkinter as tk
from tkinter import ttk
import subprocess
import speedtest

class DiagnosticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Diagnostics Assistant")
        self.root.geometry("500x600")
        self.root.config(bg="#2E3B4E")  # Dark blue background for modern feel

        # Style Configuration
        self.style = ttk.Style()
        self.style.configure("TButton",
                             font=("Arial", 12),
                             background="#4CAF50",  # Green button color
                             padding=10)
        self.style.configure("TEntry",
                             font=("Arial", 12),
                             padding=10,
                             relief="flat",  # Remove border for modern look
                             foreground="black",
                             background="#f1f1f1")  # Light background for text input
        self.style.configure("TLabel",
                             font=("Arial", 12),
                             background="#f1f1f1",  # Light background for messages
                             foreground="#333")

        # Chat History (Scrollable Frame)
        self.chat_frame = ttk.Frame(root, padding=10)
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.chat_frame, bg="#f1f1f1")
        self.scrollbar = ttk.Scrollbar(self.chat_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Entry Box for User Input
        self.entry_frame = ttk.Frame(root, padding=10)
        self.entry_frame.pack(fill=tk.X)

        self.entry = ttk.Entry(self.entry_frame, width=50)
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.entry.bind("<Return>", self.run_diagnostic)

        self.send_button = ttk.Button(self.entry_frame, text="Send", command=self.run_diagnostic)
        self.send_button.pack(side=tk.RIGHT, padx=5)

    def add_message(self, text, sender="System"):
        """Add a message to the chat."""
        bg_color = "#d9fdd3" if sender == "User" else "#ffffff"
        message = ttk.Label(
            self.scrollable_frame,
            text=f"{sender}: {text}",
            background=bg_color,
            wraplength=400,
            justify="left",
            anchor="w",
            padding=10
        )
        message.pack(fill=tk.X, pady=5, padx=10)

    def run_diagnostic(self, event=None):
        """Run diagnostic based on user input."""
        user_input = self.entry.get().strip()
        if not user_input:
            return

        # Display the user's input
        self.add_message(user_input, sender="User")
        self.entry.delete(0, tk.END)

        # Handle Commands
        commands = {
            "check connectivity": self.check_connectivity,
            "check ip": self.check_ip_config,
            "check dns": self.check_dns_resolution,
            "check latency": self.check_latency,
            "check speed": self.check_speed,
            "restart network": self.restart_network,
            "check routes": self.check_routes,
            "help": self.show_help,
        }

        func = commands.get(user_input.lower(), self.unknown_command)
        result = func()

        # Display the system's response
        self.add_message(result)

    # Diagnostic Functions
    def check_connectivity(self):
        try:
            response = subprocess.run(["ping", "-c", "4", "8.8.8.8"], capture_output=True, text=True)
            return "Network is reachable." if response.returncode == 0 else "No network connectivity."
        except Exception as e:
            return f"Error: {str(e)}"

    def check_ip_config(self):
        try:
            response = subprocess.run(["ipconfig"], capture_output=True, text=True, shell=True)
            return response.stdout
        except Exception as e:
            return f"Error: {str(e)}"

    def check_dns_resolution(self):
        try:
            response = subprocess.run(["nslookup", "google.com"], capture_output=True, text=True)
            if "Non-authoritative answer" in response.stdout:
                return "DNS resolution is working."
            else:
                return "DNS issue detected."
        except Exception as e:
            return f"Error: {str(e)}"

    def check_latency(self):
        try:
            response = subprocess.run(["ping", "-c", "4", "google.com"], capture_output=True, text=True)
            return response.stdout
        except Exception as e:
            return f"Error: {str(e)}"

    def check_speed(self):
        try:
            st = speedtest.Speedtest()
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            return f"Download Speed: {download_speed:.2f} Mbps\nUpload Speed: {upload_speed:.2f} Mbps"
        except Exception as e:
            return f"Error: {str(e)}"

    def restart_network(self):
        try:
            response = subprocess.run(["ipconfig", "/release"], shell=True, capture_output=True, text=True)
            response = subprocess.run(["ipconfig", "/renew"], shell=True, capture_output=True, text=True)
            return "Network adapter restarted successfully."
        except Exception as e:
            return f"Error: {str(e)}"

    def check_routes(self):
        try:
            response = subprocess.run(["route", "print"], capture_output=True, text=True, shell=True)
            return response.stdout
        except Exception as e:
            return f"Error: {str(e)}"

    def show_help(self):
        return """Available commands:
- check connectivity
- check ip
- check dns
- check latency
- check speed
- restart network
- check routes
- help"""

    def unknown_command(self):
        return "Unknown command. Try 'help' for a list of commands."


# Main Application Loop
if __name__ == "__main__":
    root = tk.Tk()
    app = DiagnosticsApp(root)
    root.mainloop()
