from flask import Flask, render_template, request, redirect, url_for, flash
from models import Business, directory

app = Flask(__name__)
app.secret_key = "business_dir_secret_key"


# ── Home — view all businesses ────────────────────────────────────────────────

@app.route("/")
def index():
    search_query = request.args.get("q", "").strip().lower()
    all_businesses = [b.to_dict() for b in directory.get_all()]
    
    if search_query:
        all_businesses = [b for b in all_businesses if search_query in b["name"].lower()]
    
    recent = [b.to_dict() for b in directory.get_recent()]
    categories = directory.get_categories()
    can_undo = directory.can_undo()

    return render_template(
        "index.html",
        businesses=all_businesses,
        recent=recent,
        categories=categories,
        total=directory.total_count(),
        can_undo=can_undo,
        search_query=request.args.get("q", ""),
    )


# ── Filter by category ────────────────────────────────────────────────────────

@app.route("/category/<category_name>")
def by_category(category_name):
    filtered = [b.to_dict() for b in directory.get_by_category(category_name)]
    categories = directory.get_categories()
    can_undo = directory.can_undo()

    return render_template(
        "index.html",
        businesses=filtered,
        recent=[b.to_dict() for b in directory.get_recent()],
        categories=categories,
        total=directory.total_count(),
        active_category=category_name,
        can_undo=can_undo,
    )


# ── Add a new business ────────────────────────────────────────────────────────

@app.route("/add", methods=["GET", "POST"])
def add_business():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()
        contact = request.form.get("contact", "").strip()
        founded_year = request.form.get("founded_year", "").strip()
        website = request.form.get("website", "").strip()

        if not all([name, category, location, description, contact]):
            flash("All fields are required.", "error")
            return redirect(url_for("add_business"))

        new_business = Business(name, category, location, description, contact, 
                                founded_year or None, website or None)
        directory.add_business(new_business)
        flash(f'"{name}" has been added to the directory!', "success")
        return redirect(url_for("index"))

    return render_template("add.html")


# ── Delete a business ─────────────────────────────────────────────────────────

@app.route("/delete/<int:index>", methods=["POST"])
def delete_business(index):
    removed = directory.delete_business(index)
    if removed:
        flash(f'"{removed.name}" was deleted. You can undo this action.', "warning")
    else:
        flash("Business not found.", "error")
    return redirect(url_for("index"))


# ── Undo last delete (Stack pop) ──────────────────────────────────────────────

@app.route("/undo", methods=["POST"])
def undo_delete():
    restored = directory.undo_delete()
    if restored:
        flash(f'"{restored.name}" has been restored!', "success")
    else:
        flash("Nothing to undo.", "error")
    return redirect(url_for("index"))


# ── About page ────────────────────────────────────────────────────────────────

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
