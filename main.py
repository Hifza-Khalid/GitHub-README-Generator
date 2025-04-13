import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import pandas as pd
import os

# Define fields with emojis
fields = {
    "github_banner_link": "📷 GitHub Banner Image URL",
    "username": "👤 GitHub Username",
    "Currently Working": "🛠 Currently Working On",
    "Open to Collaborate": "🤝 Collaboration Interests",
    "mail": "📧 Email Address",
    "fun_fact": "💡 Fun Fact",
    "image_octact": "🖼 Right-Side Image URL",
    "website_link": "🌐 Blog/Portfolio Link"
}

dynamic_fields = {
    "skills": " Skills💻",
    "tools": " Tools & Technologies🛠",
    "languages": " Programming Languages🌍",
    "documentation_skills": " Documentation Skills📝",
    "currently_learning": " Currently Learning📚"
}

user_data = {}
skills_list = []
tools_list = []
language_tags = []
doc_skills_rows = []
learning_rows = []


class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Splash Screen")
        self.root.geometry("600x400")
        self.root.configure(bg="#E6F7FF")

        # Load the logo image
        logo_image = Image.open("logo.png")
        logo_image = logo_image.resize((250, 250))
        self.logo = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(self.root, image=self.logo, bg="#E6F7FF")
        logo_label.pack(pady=20)

        title_label = tk.Label(self.root, text="GitHub README Generator", font=("Arial", 20, "bold"), fg="#003366", bg="#E6F7FF")
        title_label.pack(pady=10)
        loading_label = tk.Label(self.root, text="loading...", font=("Arial", 15, "bold"), fg="#003366", bg="#E6F7FF")
        loading_label.pack()

        self.root.after(3000, self.close_splash_screen)

    def close_splash_screen(self):
        self.root.destroy()


class App:
    def __init__(self, root):
        self.root = root
        root.title("GitHub README Generator")
        root.geometry("1200x1200")

        # Load background image
        self.bg_image = Image.open("background_img.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Canvas for background
        self.canvas = tk.Canvas(root, width=900, height=800)
        self.canvas.pack(fill="both", expand=True)

        # Set the background image on canvas
        self.canvas_bg = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

        # Scrollable frame on canvas
        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="#E6F7FF")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.scroll_y.pack(side="right", fill="y")

        # Repack canvas after scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)

        # Main Title
        tk.Label(self.scroll_frame, text="📄 GitHub README Generator",
                 font=("Arial", 18, "bold"), bg="#B3E0FF", fg="#003366", pady=10).pack(fill="x")

        info_frame = tk.LabelFrame(self.scroll_frame, text="Static Information",
                                   font=("Arial", 12, "bold"), bg="#E6F7FF", fg="#004d66", padx=10, pady=10)
        info_frame.pack(fill="x", padx=20, pady=10)

        self.entries = {}
        self.dynamic_counts = {}

        for key, label in fields.items():
            row = tk.Frame(info_frame, bg="#E6F7FF")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label, width=25, anchor='w', bg="#E6F7FF", font=("Arial", 10)).pack(side="left")
            entry = tk.Entry(row, width=60)
            entry.pack(side="left", padx=5)
            self.entries[key] = entry

        dyn_frame = tk.LabelFrame(self.scroll_frame, text="Dynamic Information",
                                  font=("Arial", 12, "bold"), bg="#E6F7FF", fg="#004d66", padx=10, pady=10)
        dyn_frame.pack(fill="x", padx=20, pady=10)

        for key, label in dynamic_fields.items():
            row = tk.Frame(dyn_frame, bg="#E6F7FF")
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"How many {label}?", width=25, anchor='w', bg="#E6F7FF", font=("Arial", 10)).pack(side="left")
            count_entry = tk.Entry(row, width=10)
            count_entry.pack(side="left", padx=5)
            self.dynamic_counts[key] = count_entry

        btn_frame = tk.Frame(self.scroll_frame, bg="#E6F7FF")
        btn_frame.pack(pady=10)
        self.generate_button = tk.Button(btn_frame, text="➕ Generate Inputs", command=self.generate_dynamic_inputs,
                                         bg="#3399ff", fg="white", font=("Arial", 11, "bold"))
        self.generate_button.grid(row=0, column=0, padx=10)

        self.save_button = tk.Button(btn_frame, text="💾 Save README", command=self.save_readme,
                                     state=tk.DISABLED, bg="#33cc99", fg="white", font=("Arial", 11, "bold"))
        self.save_button.grid(row=0, column=1, padx=10)

        self.output = scrolledtext.ScrolledText(self.scroll_frame, height=15, width=110, wrap=tk.WORD,
                                                font=("Consolas", 10))
        self.output.pack(padx=20, pady=10)

    def generate_dynamic_inputs(self):
        global skills_list, tools_list, language_tags, doc_skills_rows, learning_rows
        skills_list, tools_list, language_tags, doc_skills_rows, learning_rows = [], [], [], [], []

        for key in fields:
            user_data[key] = self.entries[key].get()

        for key in dynamic_fields:
            try:
                count = int(self.dynamic_counts[key].get())
            except ValueError:
                messagebox.showerror("Error", f"Please enter a valid number for {key}")
                return

            for i in range(count):
                item = simpledialog.askstring("Input", f"Enter {dynamic_fields[key][:-1]} {i + 1}")
                if not item:
                    continue

                if key == "skills":
                    skills_list.append(item)
                elif key == "tools":
                    tools_list.append(item)
                elif key == "languages":
                    lang_clean = item.replace(" ", "%20")
                    badge = f"<img src='https://img.shields.io/badge/{lang_clean}-brightgreen?style=for-the-badge&logo={item.lower()}&logoColor=white' alt='{item}' />"
                    language_tags.append(badge)
                elif key == "documentation_skills":
                    rating = simpledialog.askinteger("Rating", f"Enter rating (1-5) for {item}", minvalue=1, maxvalue=5)
                    doc_skills_rows.append(f"<tr><td>{item}</td><td>{'⭐' * rating}</td></tr>")
                elif key == "currently_learning":
                    progress = simpledialog.askinteger("Progress", f"Enter progress (1-5) for {item}", minvalue=1, maxvalue=5)
                    learning_rows.append(f"<tr><td>{item}</td><td>{'⭐' * progress}</td></tr>")

        user_data["skills_string"] = "+".join(skills_list)
        user_data["tools_string"] = ",".join(tools_list)
        user_data["language_images"] = "\n".join(language_tags)
        user_data["documentation_skills"] = "\n".join(doc_skills_rows)
        user_data["currently_learning"] = "\n".join(learning_rows)

        df = pd.DataFrame([user_data])
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "✅ Preview of Your Data:\n\n")
        self.output.insert(tk.END, df.T.to_string())
        self.save_button.config(state=tk.NORMAL)

    def save_readme(self):
        try:
            if not os.path.exists("readme_template.md"):
                messagebox.showerror("Error", "Template file 'readme_template.md' not found.")
                return

            with open("readme_template.md", "r", encoding="utf-8") as f:
                template = f.read()

            for key, value in user_data.items():
                template = template.replace("{" + key + "}", str(value))

            with open("README.md", "w", encoding="utf-8") as f:
                f.write(template)

            messagebox.showinfo("Success", "🎉 README.md generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    splash = SplashScreen(root)
    root.mainloop()

    root = tk.Tk()
    app = App(root)
    root.mainloop()
