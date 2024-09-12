import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import re
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Only for testing, use SSL verification in production


ip_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
session=requests.Session()

cdf_endpoint = "https://api.cloudflare.com/client/v4/accounts/{account_id}}/rules/lists/{list_id}/items" # Account ID and List ID

user_email=None
user_key=None
filename = None
cdf_request_headers={}


def validate_credentials():  # done
    """Validate the user's credentials."""
    email = email_entry.get()
    key = key_entry.get()


    auth_endpoint = "https://api.cloudflare.com/client/v4/user"
    auth_headers = {
            "X-Auth-Email": email,
            "X-Auth-Key": key
    }

    response=session.get(auth_endpoint,headers=auth_headers)
    global user_email
    user_email=email
    
    global cdf_request_headers
    # Replace this with your actual authentication logic.
    if response.status_code==200:
        cdf_request_headers = {
            "X-Auth-Email": email,
            "X-Auth-Key": key,
            "Content-Type": "application/json"
        }
        show_success_page()
    else:
        messagebox.showerror("Authentication Failed", "Invalid X-Auth-Email or X-Auth-Key")


def show_success_page():
    """Display a success message on a new page."""
    # Clear the current page
    for widget in root.winfo_children():
        widget.destroy()


    # Input field for selecting a .txt file
    tk.Label(root, text="Select a .txt file with IP addresses:").pack(pady=5)
    file_button = tk.Button(root, text="Browse", command=select_file)
    file_button.pack(pady=5)

    # Display selected file path
    global ip_entry
    ip_entry = tk.Entry(root, width=40)
    ip_entry.pack(pady=5)

    # Button to block IPs from file
    tk.Button(root, text="Block IPs from File", command=block_ips).pack(pady=10)

    # Input field for entering a single IP address
    tk.Label(root, text="Enter Single IP Address:").pack(pady=5)
    global single_ip_entry
    single_ip_entry = tk.Entry(root)
    single_ip_entry.pack(pady=5)

    # Button to handle single IP blocking
    tk.Button(root, text="Block Single IP", command=handle_single_ip).pack(pady=10)



def select_file():
    """Open file dialog to select a .txt file and display the file path."""
    global filename
    filename = filedialog.askopenfilename(title="Select IP List File", filetypes=[("Text files", "*.txt")])
    if filename:
        ip_entry.delete(0, tk.END)  # Clear previous file content
        ip_entry.insert(0, filename)  # Display selected filename



def handle_single_ip():
    """Handle the blocking of a single IP address."""
    single_ip = single_ip_entry.get()
    global user_email

    if re.match(ip_pattern, single_ip):
        data = [
            {
                "comment": f"Blocked By:{user_email}",
                "ip": single_ip
            }
        ]
        try:
            session.post(cdf_endpoint, headers=cdf_request_headers, data=json.dumps(data))
            messagebox.showinfo("Success", f"IP {single_ip} has been blocked.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred during blocking: {e}")
    else:
        messagebox.showerror("Error", "Invalid IP Address format.")


def block_ips():
    """Block IPs from the selected file."""
    # Validate file selection
    if not filename:
        messagebox.showerror("Error", "Please select an IP list file")
        return

    # Confirmation prompt
    confirmation = messagebox.askquestion("Confirmation", "Are you sure you want to block these IPs? This action cannot be undone.")
    if confirmation != "yes":
        return
    global user_email

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        for i in lines:
            ipaddr = i.strip()
            if re.match(ip_pattern, ipaddr):
                data = [
                    {
                        "comment": f"Blocked By:{user_email}",
                        "ip": ipaddr
                    }
                ]

                session.post(cdf_endpoint, headers=cdf_request_headers, data=json.dumps(data))
                messagebox.showinfo("Success", f"IP addresses from {filename} have been blocked.")
            else:
                messagebox.showerror("Error", f"Invalid IP address: {ipaddr}")
                continue

    except FileNotFoundError:
        messagebox.showerror("Error", "File not found: " + filename)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred during blocking: {e}")



def create_login_page():
    """Create the login page interface."""
    global email_entry, key_entry

    # X-Auth-Email Label and Entry
    tk.Label(root, text="X-Auth-Email:").pack(pady=5)
    email_entry = tk.Entry(root)
    email_entry.pack(pady=5)

    # X-Auth-Key Label and Entry
    tk.Label(root, text="X-Auth-Key:").pack(pady=5)
    key_entry = tk.Entry(root, show="*")
    key_entry.pack(pady=5)

    # Submit Button
    submit_button = tk.Button(root, text="Submit", command=validate_credentials)
    submit_button.pack(pady=10)


# Initialize main window
root = tk.Tk()
root.title("CloudFlare IP Blocker")
root.geometry("500x300")

# Create login page
create_login_page()

# Run the application
root.mainloop()


