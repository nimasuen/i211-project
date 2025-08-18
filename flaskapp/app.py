# Copyright © 2023, Indiana University
# BSD 3-Clause License

# Copyright © 2023-2024, Indiana University
# BSD 3-Clause License

import re
from flaskapp import database
from csv import DictReader, DictWriter
from datetime import date, timedelta
from operator import itemgetter
from random import randint
from typing import Optional, List, Dict

from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)


def validate_date(date_string: str) -> str:
    """Return the string if it's in ISO format, or '' otherwise."""
    try:
        date.fromisoformat(date_string)
    except ValueError:
        return ""
    return date_string


def validate_phone(phone_string: str) -> str:
    """Return the 10 digits in a phone number, or '' otherwise."""
    new_phone = re.sub("[^0-9]", "", phone_string)
    if len(new_phone) != 10:
        return ""
    return new_phone


# def load_equipment() -> List[Dict[str, str]]:
#     """Return a list[dict] of the equipment sorted by name"""
#     with open("equipment.csv") as csvf:
#         data = list(DictReader(csvf))
        
#         data.sort(key=itemgetter("name"))
#         return data



@app.route("/")
def render_index():
    return render_template("index.html")


@app.route("/people/")
def render_people_page():
    return render_template("people.html", people=database.get_people())


def inspect_person(person: Dict[str, str]) -> None:
    """!mutates: any value that does not pass is replaced with empty string"""

    person["date_of_birth"] = validate_date(person["date_of_birth"])
    person["mobile_phone_number"] = validate_phone(person["mobile_phone_number"])

    if person["role"] not in ("staff", "member"):
        person["role"] = ""


@app.route("/people/add/", methods=["GET", "POST"])
def render_add_person():
    if request.method == "GET":
        return render_template("person_form.html", person=dict())

    # POST
    new_person = dict(request.form)

    inspect_person(new_person)
    if any(v == "" for v in new_person.values()):
        # If any error occurred, tell the user to try again
        return render_template("person_form.html", person=database.add_person, alert=True)

    # We didn't re-render, so we can save a new copy of the CSV
    # As an exercise: what *low-probability edge case* am I ignoring?
    new_person["id"] = str(randint(100_000, 10_000_000))
    all_people = database.get_people() + [new_person]

    return redirect(url_for("render_people_page"))


@app.route("/people/<person_id>/edit/", methods=["GET", "POST"])
def render_edit_person(person_id: Optional[str] = None):
    if request.method == "GET":
        return render_template(
            "person_form.html", person_id=person_id, person=database.get_person(person_id)
        )

    # POST
    updated_person = dict(request.form)
    inspect_person(updated_person)

    if any(v == "" for v in updated_person.values()):
        return render_template("person_form.html", person_id=person_id, person=database.update_person, alert=True)

    # Validation success: Update the row with matching person_id
    all_people = database.get_people()
    iid = [p["id"] for p in all_people].index(person_id)
    updated_person["id"] = person_id
    all_people[iid] = updated_person

    with open("people.csv", "w") as csvf:
        writer = DictWriter(csvf, fieldnames=updated_person.keys())
        writer.writeheader()
        writer.writerows(all_people)

    return redirect(url_for("render_one_person", person_id=person_id))


@app.route("/people/<person_id>/")
def render_one_person(person_id: Optional[str] = None):
    return render_template("person.html", person_id=person_id, person=database.get_person(person_id))


@app.route("/equipment/")
def render_equipment_page():
    return render_template("equipment.html", equipment=database.get_all_items())


@app.route("/equipment/<item_id>/", methods=["GET", "POST"])
def render_one_item(item_id: Optional[str] = None):
    item_details = database.get_one_item(item_id)
    rental_status = item_details.get("rental_status", "available")
    renter_name = item_details.get("renter_name", "")
    checkout_date = item_details.get("checkout_date", "")
    due_date = item_details.get("due_date", "")

    if rental_status == "available":
        # Get all members (not staff) for the dropdown
        members = [person for person in database.get_people() if person["role"] != "staff"]
        if request.method == "POST":
            # Handle the rental process (e.g., update rental status, due date, etc.)
            selected_member_id = request.form.get("member_id")
            return redirect(url_for("render_one_item", item_id=item_id))

        return render_template(
            "item.html",  # Use the same template for both scenarios
            item_id=item_id,
            item=item_details,
            members=members,
            rental_status=rental_status,
        )
    else:
        if request.method == "POST":
            return redirect(url_for("render_one_item", item_id=item_id))

        return render_template(
            "item.html",  # Use the same template for both scenarios
            item_id=item_id,
            item=item_details,
            renter_name=renter_name,
            checkout_date=checkout_date,
            due_date=due_date,
            rental_status=rental_status,
        )

@app.route("/equipment/<item_id>/rent/", methods=["POST"])
def rent_equipment(item_id: Optional[str] = None):
    if request.method == "POST":
        rental_info = {
            "item_id": item_id,
            "checkout_date": date.today(),  # Current date

            "due_date": date.today() + timedelta(days=14),  

            "due_date": date.today() + timedelta(days=14),  # 2 weeks from today

        }

        all_items = database.get_all_items()
        for item in all_items:
            if item["id"] == item_id:
                item["currently_available"] = False
                break

        return redirect(url_for("render_one_item", item_id=item_id))
    
@app.route("/equipment/<item_id>/return/", methods=["POST"])
def return_equipment(item_id: Optional[str] = None):
    if request.method == "POST":
        rental_info = {
            "item_id": item_id,
            "return_date": date.today(),  # Current date
        }
        all_items = database.get_all_items()
        for item in all_items:
            if item["id"] == item_id:
                item["currently_available"] = True
                break
        
        return redirect(url_for("render_one_item", item_id=item_id))



    


@app.route("/equipment/add/", methods=["GET", "POST"])
def render_add_equipment():
    if request.method == "GET":
        return render_template("item_form.html", item=dict())

    # POST: assume no bad data
    new_item = dict(request.form)
    new_item["image_path"] = "images/null_image.jpg"
    new_item["id"] = str(randint(100_000, 10_000_000))
    new_item["item_condition"] = request.form.get("item_condition", "")

    return redirect(url_for("render_equipment_page"))


@app.route("/equipment/<item_id>/edit/", methods=["GET", "POST"])
def render_edit_equipment(item_id: Optional[str] = None):
    if request.method == "GET":
        return render_template("item_form.html", item_id=item_id, item=database.get_one_item(item_id))

    # POST
    updated = dict(request.form)

    # Keep the `id` and `image_path` the same from before.
    old_data = database.update_one_item(item_id)
    updated["id"] = old_data["id"]
    updated["image_path"] = old_data["image_path"]

    # Find the index where the person_id matches and update it
    all_items = database.get_all_items()
    iid = [p["id"] for p in all_items].index(item_id)
    all_items[iid] = updated


    return redirect(url_for("render_one_item", item_id=item_id))