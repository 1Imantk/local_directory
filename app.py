from flask import Flask, render_template, request, redirect, url_for, flash
from models import Business
from data import directory

app = Flask(__name__)
app.secret_key = "business_dir_secret_key"


# ── Home — view all businesses ────────────────────────────────────────────────

PER_PAGE = 6

@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    search_query = request.args.get("q", "").strip().lower()
    sort_by = request.args.get("sort", "newest")
    all_businesses = [b.to_dict() for b in directory.get_all()]
    
    if search_query:
        all_businesses = [b for b in all_businesses if search_query in b["name"].lower()]
    
    if sort_by == "oldest":
        all_businesses = sorted(all_businesses, key=lambda b: b["registered_at"])
    elif sort_by == "az":
        all_businesses = sorted(all_businesses, key=lambda b: b["name"].lower())
    else:
        all_businesses = sorted(all_businesses, key=lambda b: b["registered_at"], reverse=True)
    
    total_businesses = len(all_businesses)
    total_pages = max(1, (total_businesses + PER_PAGE - 1) // PER_PAGE)
    page = max(1, min(page, total_pages))
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    businesses = all_businesses[start:end]
    
    recent = [b.to_dict() for b in directory.get_recent()]
    categories = directory.get_categories()
    category_counts = directory.get_category_counts()
    can_undo = directory.can_undo()

    return render_template(
        "index.html",
        businesses=businesses,
        recent=recent,
        categories=categories,
        category_counts=category_counts,
        total=directory.total_count(),
        can_undo=can_undo,
        search_query=request.args.get("q", ""),
        sort_by=sort_by,
        page=page,
        total_pages=total_pages,
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

        if directory.name_exists(name):
            flash(f'A business named "{name}" already exists. Please use a different name.', "error")
            return redirect(url_for("add_business"))

        new_business = Business(name, category, location, description, contact, 
                                founded_year or None, website or None)
        directory.add_business(new_business)
        
        business_data = {
            "name": name,
            "category": category,
            "location": location,
            "description": description,
            "contact": contact,
            "founded_year": founded_year or None,
            "website": website or None,
        }
        return render_template("confirmation.html", business=business_data)

    return render_template("add.html")


# ── Business detail page ──────────────────────────────────────────────────────

@app.route("/business/<int:business_id>")
def business_detail(business_id):
    business = directory.get_by_id(business_id)
    if not business:
        flash("Business not found.", "error")
        return redirect(url_for("index"))
    return render_template("business_detail.html", business=business.to_dict())


# ── Edit a business ───────────────────────────────────────────────────────────

@app.route("/edit/<int:business_id>", methods=["GET", "POST"])
def edit_business(business_id):
    business = directory.get_by_id(business_id)
    if not business:
        flash("Business not found.", "error")
        return redirect(url_for("index"))

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
            return redirect(url_for("edit_business", business_id=business_id))

        existing_name = any(b.name.lower() == name.lower() and b.id != business_id for b in directory.get_all())
        if existing_name:
            flash(f'A business named "{name}" already exists. Please use a different name.', "error")
            return redirect(url_for("edit_business", business_id=business_id))

        updated = directory.update_business(
            business_id, name, category, location, description, contact,
            founded_year or None, website or None
        )
        if updated:
            flash(f'"{name}" has been updated successfully!', "success")
            return redirect(url_for("business_detail", business_id=business_id))
        flash("Failed to update business.", "error")
        return redirect(url_for("index"))

    return render_template("edit.html", business=business.to_dict())


# ── Rate a business ─────────────────────────────────────────────────────────

@app.route("/rate/<int:business_id>", methods=["POST"])
def rate_business(business_id):
    business = directory.get_by_id(business_id)
    if not business:
        flash("Business not found.", "error")
        return redirect(url_for("index"))
    
    stars = request.form.get("stars", type=int)
    if stars and 1 <= stars <= 5:
        business.add_rating(stars)
        flash(f'Thank you! You rated "{business.name}" {stars} star{"s" if stars > 1 else ""}.', "success")
    else:
        flash("Please select a valid rating (1-5 stars).", "error")
    
    return redirect(url_for("business_detail", business_id=business_id))


# ── Toggle business status ────────────────────────────────────────────────────

@app.route("/toggle-status/<int:business_id>", methods=["POST"])
def toggle_status(business_id):
    business = directory.get_by_id(business_id)
    if not business:
        flash("Business not found.", "error")
        return redirect(url_for("index"))
    
    business.is_open = not business.is_open
    status = "Open" if business.is_open else "Closed"
    flash(f'{business.name} is now {status}.', "success")
    return redirect(url_for("business_detail", business_id=business_id))


# ── Delete a business ─────────────────────────────────────────────────────────

@app.route("/delete/<int:business_id>", methods=["POST"])
def delete_business(business_id):
    for i, b in enumerate(directory.get_all()):
        if b.id == business_id:
            removed = directory.delete_business(i)
            flash(f'"{removed.name}" was deleted. You can undo this action.', "warning")
            return redirect(url_for("index"))
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


# ── Error pages ───────────────────────────────────────────────────────────────

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
