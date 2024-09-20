from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_required_grades(prelim_grade):
    # Constants
    target_grade = 75
    deans_lister_grade = 90
    prelim_weight = 0.20
    midterm_weight = 0.30
    final_weight = 0.50

    # Calculate the contribution of the Prelim Grade
    prelim_contribution = prelim_grade * prelim_weight
    
    # Calculate the remaining contribution needed from Midterm and Final grades
    remaining_contribution_needed = target_grade - prelim_contribution

    # Calculate the minimum required Midterm and Final grades
    min_midterm_grade = remaining_contribution_needed / (midterm_weight + final_weight)
    min_final_grade = min_midterm_grade

    # Check if it's mathematically possible to pass
    max_possible_midterm_and_final = (100 * midterm_weight) + (100 * final_weight)
    if remaining_contribution_needed > max_possible_midterm_and_final:
        return (f"Prelim Grade: {prelim_grade}\nIt is difficult to pass regardless of your midterm and final grades.",
                "It is not possible to be a Dean’s Lister.")

    # Calculate required midterm and final grades to pass
    min_midterm_grade = min(max(min_midterm_grade, 0), 100)
    min_final_grade = min(max(min_final_grade, 0), 100)

    # Calculate the remaining contribution needed from Midterm and Final grades
    deans_contribution_needed = deans_lister_grade - prelim_contribution

    # Calculate the minimum required Midterm and Final grades
    deans_midterm_grade = deans_contribution_needed / (midterm_weight + final_weight)
    deans_final_grade = deans_midterm_grade

    # Ensure Dean's Lister grades are within bounds
    deans_midterm_grade = min(max(deans_midterm_grade, 0), 100)
    deans_final_grade = min(max(deans_final_grade, 0), 100)

    # Check Dean's Lister qualification
    if deans_midterm_grade < 100 and deans_final_grade < 100:
        deans_message = (f"The required grade for you to be a Dean’s Lister is: {deans_midterm_grade:.2f} (Midterm) and {deans_final_grade:.2f} (Finals).")
    else:
        deans_message = "It is not possible to be a Dean’s Lister."

    pass_message = (f"Prelim Grade: {prelim_grade} - \n"
                    f"Required Midterm Grade: {min_midterm_grade:.2f} - \n"
                    f"Required Final Grade: {min_final_grade:.2f} - \n"
                    "You have a chance to pass!")

    return pass_message, deans_message

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get the Prelim Grade from the form input
            prelim_grade = float(request.form['prelim_grade'])

            # Validate the Prelim Grade
            if prelim_grade < 0 or prelim_grade > 100:
                error_message = "Grade must be between 0 and 100."
                return render_template('index.html', error=error_message)

            # Calculate the required grades and Dean's Lister message
            pass_message, deans_message = calculate_required_grades(prelim_grade)

            # Pass the results to the HTML template
            return render_template('index.html', 
                                   prelim_grade=prelim_grade,
                                   pass_message=pass_message,
                                   deans_message=deans_message)

        except ValueError:
            error_message = "Please enter a valid number."
            return render_template('index.html', error=error_message)

    # Render the form initially
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
