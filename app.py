from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Sample static data for people
people = [
    {"id": "#1", "name": "Krish", "tickets_assigned": []},
    {"id": "#2", "name": "Alan", "tickets_assigned": []},
    {"id": "#3", "name": "Mohan", "tickets_assigned": []},
    {"id": "#4", "name": "Kumar", "tickets_assigned": []},
    {"id": "#5", "name": "Charlie", "tickets_assigned": []}
]

# Sample data for tickets
tickets = []

# Counter for round robin ticket assignment
round_robin_counter = 0

# Function to assign a ticket based on Round Robin Principle
def assign_ticket(issue_description, raised_by):
    global round_robin_counter
    assigned_to = people[round_robin_counter]["id"]
    ticket_id = f"#{len(tickets) + 1}"
    
    ticket = {
        "id": ticket_id,
        "issue_description": issue_description,
        "assigned_to": assigned_to,
        "raised_by": raised_by
    }
    
    tickets.append(ticket)
    people[round_robin_counter]["tickets_assigned"].append(ticket_id)
    
    # Update the round robin counter
    round_robin_counter = (round_robin_counter + 1) % len(people)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_ticket', methods=['POST'])
def submit_ticket():
    if request.method =="POST":

        issue_description = request.form['issue_description']
        raised_by = request.form['raised_by']

        if int(raised_by) > 5:
            return jsonify({"message": "No UserID found"}), 400
        
        # Call assign_ticket function
        assign_ticket(issue_description, raised_by)
        
        return jsonify({
            "message": "Ticket assigned successfully",
            "success": True,
            "data": {
                "ticket_id" : len(tickets),
                "assigned_to" : tickets[::-1][0]["assigned_to"]
            }
        }), 201

@app.route('/people', methods=['GET'])
def get_people():
    return jsonify(people)

@app.route('/tickets', methods=['GET'])
def get_tickets():
    return jsonify(tickets)

if __name__ == '__main__':
    app.run(debug=True)
