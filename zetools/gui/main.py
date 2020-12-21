import tkinter as tk
import zetools

# Define colour scheme;
col_dark = "#022c43"
col_mid = "#053f5e"
col_light = "#115173"
col_text = "white"
col_emph = "#ffd700"

# Configure base window;
window = tk.Tk()
window.configure(background=col_dark, bd=0, padx=5, pady=5)
window.title("Zetools")
window.geometry("750x400")

# Build the search inputs section;
lbf_search_criteria = tk.LabelFrame(text="Search Criteria", bd=0, bg=col_dark, fg=col_text, padx=5, pady=5)

lbl_includes_anywhere = tk.Label(master=lbf_search_criteria, text="includes anywhere:", fg=col_text, bg=col_dark)
lbl_includes_anywhere.grid(row=1, column=1, sticky="e")
ent_includes_anywhere = tk.Entry(master=lbf_search_criteria, fg=col_emph, bg=col_light, width=80, bd=0)
ent_includes_anywhere.grid(row=1, column=2)

lbl_includes_in_title = tk.Label(master=lbf_search_criteria, text="includes in title:", fg=col_text, bg=col_dark)
lbl_includes_in_title.grid(row=2, column=1, sticky="e")
ent_includes_in_title = tk.Entry(master=lbf_search_criteria, fg=col_emph, bg=col_light, width=80, bd=0)
ent_includes_in_title.grid(row=2, column=2)

lbl_excludes_everywhere = tk.Label(master=lbf_search_criteria, text="excludes everywhere:", fg=col_text, bg=col_dark)
lbl_excludes_everywhere.grid(row=3, column=1, sticky="e")
ent_excludes_everywhere = tk.Entry(master=lbf_search_criteria, fg=col_emph, bg=col_light, width=80, bd=0)
ent_excludes_everywhere.grid(row=3, column=2)

lbl_excludes_in_title = tk.Label(master=lbf_search_criteria, text="excludes in title:", fg=col_text, bg=col_dark)
lbl_excludes_in_title.grid(row=4, column=1, sticky="e")
ent_excludes_in_title = tk.Entry(master=lbf_search_criteria, fg=col_emph, bg=col_light, width=80, bd=0)
ent_excludes_in_title.grid(row=4, column=2)


def handle_search():
    """Handler for search button press."""
    # Grab the search terms;
    terms = {
        'includes_anywhere': ent_includes_anywhere.get(),
        'includes_in_title': ent_includes_in_title.get(),
        'excludes_everywhere': ent_excludes_everywhere.get(),
        'excludes_in_title': ent_excludes_in_title.get()
    }
    zetools.run_search(terms)


btn_search = tk.Button(master=lbf_search_criteria, text="Search", fg="white", bg=col_light, bd=0, padx=10,
                       command=handle_search)
btn_search.grid(column=3, row=1, rowspan=4)

lbf_search_criteria.grid(row=1, column=1)

window.mainloop()
