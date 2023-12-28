import tkinter as tk
from tkinter import messagebox
import subprocess

def submit_form():
    username = username_entry.get()
    password = password_entry.get()
    search_term = search_term_entry.get()
    company_name = company_entry.get()
    num_pages = num_pages_entry.get()
    personalized_message = message_entry.get("1.0", "end-1c")

    # Validate if all fields are filled
    if not all([username, password, search_term, company_name, num_pages, personalized_message]):
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    # Call your linkedin.py script with these parameters using subprocess
    command = ["python", "linkedin.py", username, password, search_term, company_name, num_pages, personalized_message]
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Rest of the GUI code remains the same as provided in the previous example...
root = tk.Tk()
root.title("LinkedIn Automation GUI")

fields = ["Username", "Password", "Search term", "Company", "Number of pages", "Personalized message"]
for idx, field in enumerate(fields):
    label = tk.Label(root, text=field)
    label.grid(row=idx, column=0, padx=10, pady=5)

username_entry = tk.Entry(root)
password_entry = tk.Entry(root, show="*")
search_term_entry = tk.Entry(root)
company_entry = tk.Entry(root)
num_pages_entry = tk.Entry(root)
message_entry = tk.Text(root, height=5, width=30)

username_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)
search_term_entry.grid(row=2, column=1)
company_entry.grid(row=3, column=1)
num_pages_entry.grid(row=4, column=1)
message_entry.grid(row=5, column=1)

submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()