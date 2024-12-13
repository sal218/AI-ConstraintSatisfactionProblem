from collections import deque
from tkinter import *
from tkinter import messagebox

def canada_map():
    # Define a dictionary that maps provinces (keys) to the list of neighboring provinces (values)
    return {
        'Alberta': ['British Columbia', 'Saskatchewan', 'Northwest Territories'],
        'British Columbia': ['Alberta', 'Yukon', 'Northwest Territories'],
        'Manitoba': ['Saskatchewan', 'Ontario', 'Nunavut'],
        'New Brunswick': ['Quebec', 'Nova Scotia'],
        'Newfoundland and Labrador': ['Quebec'],
        'Nova Scotia': ['New Brunswick'],
        'Ontario': ['Manitoba', 'Quebec'],
        'Prince Edward Island': ['New Brunswick', 'Nova Scotia'],
        'Quebec': ['Ontario', 'Newfoundland and Labrador', 'New Brunswick'],
        'Saskatchewan': ['Alberta', 'Manitoba', 'Northwest Territories'],
        'Northwest Territories': ['Yukon', 'Nunavut', 'Saskatchewan', 'Alberta'],
        'Nunavut': ['Manitoba', 'Northwest Territories'],
        'Yukon': ['British Columbia', 'Northwest Territories']
    }


# function to map provinces to a list of colors for its domain
def initializeVariableDomains(canada_map, colors, userInitializedDomainSize):
    # map the province from the canada_map dictionary to a list of possible colors that will make up the domain. This is done by slicing the 
    # the number of colors based on the user input
    return {province : colors[:userInitializedDomainSize] for province in canada_map.keys()}


# function to set up constraint to ensure consistency (no two neighboring provinces can have same color)
def setConstraint(province, color, assignedValue, canada_map):
    # the for loop will retreive a list of neighboring provinces for the current province (the value portion of the canada_map dict)
    for adjacentProvince in canada_map[province]:
        #check if the neighboring province has the same color assigned
        if adjacentProvince in assignedValue and assignedValue[adjacentProvince] == color:
            print(f"Conflict: {province} and {adjacentProvince} both assigned {color}")  # debug line 
            return False
    return True

# Arc consistency function to prune domains based on assignments
def arc_consistency(canada_map, domains, assignment):
    # Initialize the queue with arcs (province, adjacentProvince)
    mainQueue = deque([(province, adjacentProvince) for province in canada_map for adjacentProvince in canada_map[province]])
    
    while mainQueue:
        province, adjacentProvince = mainQueue.popleft()

        #we use this to skip the pruning of the current provinces domain. It has only one color now since its been assigned one
        if province in assignment:
            provinceValue = assignment[province]
            
            # Remov the assigned color from the neighbor's domain
            if provinceValue in domains[adjacentProvince]:
                domains[adjacentProvince].remove(provinceValue)
                print(f"Pruned {provinceValue} from {adjacentProvince}'s domain due to constraint violation with {province}")  # Debugging line

            # If the neighbor has no colors left, return failure
            if not domains[adjacentProvince]:
                print(f"Failure: No colors left for {adjacentProvince}")
                return False

            # Re-add neighbors only if domain was modified
            for neighbor in canada_map[adjacentProvince]:
                # skip adding in the current province and neighbor 
                if neighbor != province and neighbor not in assignment:
                    mainQueue.append((neighbor, adjacentProvince))

    return True

# Backtracking search to find valid assignments for provinces (Start of the backtrack search algo)
def backtracking_search(domains, canada_map):
    return backtrack({}, domains, canada_map)

# Recursive backtracking function
def backtrack(assignment, domains, canada_map):
    # base case for recursion. Checks if all provinces have been assigned a color. (Essentially signaling algo has found solution)
    if len(assignment) == len(canada_map):
        return assignment

    # call select_unassigned_province as our current province 
    province = select_unassigned_province(assignment, domains)

    for color in domains[province]:
        # call the setConstraint function to determine consistency with our constraint.
        if setConstraint(province, color, assignment, canada_map):
            # assign a color to the province 
            assignment[province] = color
            print(f"Assigned {color} to {province}, Current Assignment: {assignment}")  # Debugging line
            
            # Once a color is assigned, reduce its domain to just that color
            domain_copy = {} # this dictionary will hold the modified domains
            for prov, dom in domains.items():
                if prov in assignment:
                    # if a province has been assigned a color, its domain will be reduced to just be that color (ex: { 'Alberta' : 'Red')
                    domain_copy[prov] = [assignment[prov]]
                else:
                    # otherwise we should jsut make a copy of the current domain
                    domain_copy[prov] = dom[:]

            # checking if arc consistency returns true 
            if arc_consistency(canada_map, domain_copy, assignment):
                result = backtrack(assignment, domain_copy, canada_map)
                if result:
                    return result
            del assignment[province]  # Undo the assignment (backtrack)
    
    print(f"Backtracking on {province}")  # Debugging line
    return None

def remaining_values(province, domains):
    return len(domains[province])

# helper to identify which provinces have not been assgined a color (MRV from lectures)
def select_unassigned_province(assignment, domains):
    # filters out any provinces that already have a color assigned to them.
    unassigned_provinces = [province for province in domains if province not in assignment]
    # we begin with the first unassigned province
    minimum_province = unassigned_provinces[0]
    # then loop through the rest
    for province in unassigned_provinces[1:]:
        if remaining_values(province,domains) < remaining_values(minimum_province,domains):
            minimum_province = province
    return minimum_province


def run_map_coloring_algo():
    # user input     
    try:
        userInput_int = int(entry.get())
        if userInput_int < 1 or userInput_int > 20:
            messagebox.showerror("User Inputer Error", "Please enter a number that is between 1 and 20")
            return
    except ValueError:
        messagebox.showerror("User Input Error","You did not enter in a valid integer")
        return


    # a list of available colors 
    colors = ['Red', 'Blue', 'Orange', 'Green', 'Yellow', 'Purple', 'Pink', 'Brown', 'Black', 'White', 
            'Gray', 'Violet', 'Indigo', 'Teal', 'Magenta', 'Cyan', 'Turquoise', 'Maroon', 'Beige', 'Lavender']

    # if user enters integer larger than available colors, default to maximum number
    if userInput_int > len(colors):
        userInput_int = len(colors)

    # calls the canada_map() function
    canada_map_data = canada_map()

    # call the initialize_Domains function which stores the dictionary that holds the provinces/territories and their domain values based on user input
    domains = initializeVariableDomains(canada_map_data, colors, userInput_int)

    # Run the backtracking search
    result = backtracking_search(domains, canada_map_data)

    # we will clear the previous window if anything was there
    for widget in finalResult.winfo_children():
        widget.destroy()

    if result:
        for province, color in result.items():
            # Create a frame to hold both the province and color on the same line
            province_frame = Frame(finalResult)
            province_frame.pack(anchor='w')  # Pack the frame

            # Label the province in black
            province_label = Label(province_frame, text=f"{province}: ", fg="black")
            province_label.pack(side=LEFT)

            # Dynamically label the assigned color based on its color
            color_label = Label(province_frame, text=f"{color}", fg=color.lower())
            color_label.pack(side=LEFT)
    else:
        fail_label = Label(finalResult, text="The program failed to find a complete solution", fg="red")
        fail_label.pack()


# this will be our main GUI window utilizing tkinter 
root_window = Tk()
root_window.title("Canada Map Coloring UI")



# instruction for the user 
instruction_note = Label(root_window, text = "Please enter a number of colors for the domain (1-20): ")
instruction_note.pack()


# pass the user entry into the field
entry = Entry(root_window)
entry.pack()

# create a button for the user to click to run program from GUI
run_button = Button(root_window, text="Run Map Coloring CSP", command=run_map_coloring_algo)
run_button.pack()

# this label will be used to display our results 
finalResult = Label(root_window, text="")
finalResult.pack()

# start the tkinter event loop. This basically lets the GUI remain on the screen and not disappear immediately. 
root_window.mainloop()



