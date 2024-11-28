from py3dbp import Bin, Item, Painter
import tkinter as tk
from tkinter import ttk, messagebox
import random
from run_algorithm import run_packing_algorithm
import re

items = []
# Define a list of colors for parcels
parcel_colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'magenta', 'lime', 'teal', 'navy']


# def visualize_packing(bins):
#     # Step 3: Visualize the bin using Painter
#     for bin_obj in bins:
#         painter = Painter(bin_obj)
#         fig = painter.plotBoxAndItems(
#             title=bin_obj.partno,
#             alpha=0.8,
#             write_num=False,
#             fontsize=10
#         )
#         fig.show()


# Function to validate if the value is non-negative
def validate_non_negative(value):
    try:
        return float(value) >= 0
    except ValueError:
        return False

# Function to validate inputs within a specific range
def validate_range(value, min_value, max_value):
    try:
        value = float(value)
        return min_value <= value <= max_value
    except ValueError:
        return False

# Function to validate all input fields
def validate_inputs(*args):
    for value in args:
        if not value or not validate_non_negative(value):
            return False
    return True

# Function to handle the selection from the dropdown
def select_algorithm():
    selected_algo = algo_combobox.get()
    selected_option_label.config(text=f"Selected Algorithm: {selected_algo}")
    create_button.config(state=tk.NORMAL if selected_algo else tk.DISABLED)

def create_boxes():
    global container_details_list  # Declare as global so it's accessible everywhere
    global items  # Declare items as global to clear it when new containers are created

    # Clear the items list
    items = []

    num_boxes = num_boxes_entry.get()
    container_length = container_length_entry.get()
    container_width = container_width_entry.get()
    container_height = container_height_entry.get()
    max_weight = container_max_weight_entry.get()

    if not validate_inputs(num_boxes, container_length, container_width, container_height, max_weight):
        messagebox.showwarning("Invalid Input", "Please enter valid non-negative numbers for all fields.")
        return

    # Validate container dimensions
    if not validate_range(container_length, 0, 120) or not validate_range(container_width, 0, 150) or not validate_range(container_height, 0, 180):
        messagebox.showwarning("Invalid Dimensions", "Length must be between 0-120 cm, Width between 0-150 cm, and Height between 0-180 cm.")
        return

    # Initialize the container details list
    container_details_list = []
    num_boxes = int(num_boxes)
    container_length = float(container_length)
    container_width = float(container_width)
    container_height = float(container_height)
    max_weight = float(max_weight)

    # Open the file to write the container details
    with open("containers.txt", "w") as file:
        for i in range(1, num_boxes + 1):
            container_name = f"container_{i}"
            container_details = (container_name, (container_length, container_width, container_height), max_weight)
            container_details_list.append(container_details)
            
            # Write each container record to the file in the specified format
            file.write(f"{container_name}, ({container_length} , {container_width} , {container_height}), {max_weight}\n")

    # Confirm container creation with a message on the UI
    messagebox.showinfo("Containers Created", f"{num_boxes} containers with dimensions {container_length}x{container_width}x{container_height} (cm) have been successfully created.")

    # Clear the parcels.txt file before entering new parcels
    with open('parcels.txt', 'w') as file:
        pass  # Empty the file

    show_frame(parcel_frame)




# Function to clear all the input fields
def clear_fields():
    # Clear fields in the main frame (Container Input Form)
    num_boxes_entry.delete(0, tk.END)
    container_length_entry.delete(0, tk.END)
    container_width_entry.delete(0, tk.END)
    container_height_entry.delete(0, tk.END)
    container_max_weight_entry.delete(0, tk.END)

    # Clear fields in the parcel frame (Parcel Input Form)
    num_parcels_entry.delete(0, tk.END)
    parcel_length_low_entry.delete(0, tk.END)
    parcel_length_high_entry.delete(0, tk.END)
    parcel_width_low_entry.delete(0, tk.END)
    parcel_width_high_entry.delete(0, tk.END)
    parcel_height_low_entry.delete(0, tk.END)
    parcel_height_high_entry.delete(0, tk.END)
    parcel_weight_low_entry.delete(0, tk.END)
    parcel_weight_high_entry.delete(0, tk.END)




def add_manual_parcel(length, width, height, weight):
    global items  # Declare items as a global variable to access the existing items list

    # Validate the user input
    if not (length and width and height and weight):
        messagebox.showwarning("Invalid Input", "All fields are required.")
        return

    try:
        length = int(length)
        width = int(width)
        height = int(height)
        weight = int(weight)
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter valid numbers for Length, Width, Height, and Weight.")
        return

    # Get the dimensions of the first container to compare with the parcel dimensions
    container_length, container_width, container_height = container_details_list[0][1]

    # Validation to ensure the parcel dimensions are not greater than the container dimensions
    if length > container_length or width > container_width or height > container_height:
        messagebox.showwarning("Invalid Parcel Size", "The parcel's dimensions exceed the container's dimensions. Please adjust the parcel size.")
        return
    
    # Validation to ensure the parcel dimensions are not greater than the container dimensions
    if length < 1 or width < 1 or height < 1:
        messagebox.showwarning("Invalid Parcel Size", "The parcel's dimensions should be positive.")
        return

    # Generate the part number automatically based on the current number of items
    part_no = f"item_{len(items) + 1}"


    # Randomly choose a color for the parcel
    color = random.choice(parcel_colors)
    # Add the parcel to the global items list
    items.append((part_no, (length, width, height), weight, 1, 100, True, color))

    # Append the parcel details to the parcels.txt file without overwriting existing data
    with open("parcels.txt", "a") as file:  # Open file in append mode to add data without erasing existing content
        file.write(f"{part_no}, ({length} * {width} * {height}), {weight}\n")

    # Display success message
    messagebox.showinfo("Success", f"Parcel '{part_no}' added successfully!")


def save_parcels():
    global items  # Ensure we modify the global items list


    # Continue with random parcel generation if no manual parcels were added
    num_parcels = num_parcels_entry.get()
    length_low = parcel_length_low_entry.get()
    length_high = parcel_length_high_entry.get()
    width_low = parcel_width_low_entry.get()
    width_high = parcel_width_high_entry.get()
    height_low = parcel_height_low_entry.get()
    height_high = parcel_height_high_entry.get()
    weight_low = parcel_weight_low_entry.get()
    weight_high = parcel_weight_high_entry.get()

    if not validate_inputs(num_parcels, length_low, length_high, width_low, width_high, height_low, height_high, weight_low, weight_high):
        messagebox.showwarning("Invalid Input", "Please enter valid non-negative numbers for all fields.")
        return

    # Check that low values are not greater than high values
    if float(length_low) > float(length_high) or float(width_low) > float(width_high) or float(height_low) > float(height_high) or float(weight_low) > float(weight_high):
        messagebox.showwarning("Invalid Range", "Low values cannot be greater than High values.")
        return
    
    # Additional condition to check that parcel dimensions are at least 1 unit smaller than the container dimensions
    for container in container_details_list:
        _, (container_length, container_width, container_height), _ = container
        if int(length_high) >= container_length or int(width_high) >= container_width or int(height_high) >= container_height:
            messagebox.showwarning("Invalid Parcel Size", "High values must be at least 1 cm smaller than the container dimensions.")
            return
        
    # Additional condition to check that parcel dimensions are at least 1 unit smaller than the container dimensions
    for container in container_details_list:
        _, (container_length, container_width, container_height), _ = container
        if int(length_low) >= container_length or int(width_low) >= container_width or int(height_low) >= container_height:
            messagebox.showwarning("Invalid Parcel Size", "High values must be at least 1 cm smaller than the container dimensions.")
            return

    # Convert inputs to integers/floats for further use
    num_parcels = int(num_parcels)
    length_low = int(length_low)
    length_high = int(length_high)
    width_low = int(width_low)
    width_high = int(width_high)
    height_low = int(height_low)
    height_high = int(height_high)
    weight_low = int(weight_low)
    weight_high = int(weight_high)

    with open("parcels.txt", "a") as file:  # Open file in write mode to start fresh
        for i in range(num_parcels):
            length = random.randint(length_low, length_high)
            width = random.randint(width_low, width_high)
            height = random.randint(height_low, height_high)
            weight = random.randint(weight_low, weight_high)
            part_no = f"item_{len(items) + 1}"  # Automatically generate part number

            # Randomly choose a color for the parcel
            color = random.choice(parcel_colors)
            items.append((part_no, (length, width, height), weight, 1, 100, True, color))

            # Save each parcel record to the file in the specified format
            file.write(f"{part_no}, ({length} , {width} , {height}), {weight}\n")

    messagebox.showinfo("Success", "Random parcel records saved successfully.")
    
    # Switch to the output frame to display results
    run_algorithm_and_show_results()


# Function to run the algorithm and display the results
def run_algorithm_and_show_results():
    global container_details_list  # Ensure we use the global variable

    if not container_details_list:  # Check if the container list has been created
        messagebox.showerror("Error", "No containers have been created. Please create containers first.")
        return

    results = run_packing_algorithm(items,container_details_list)  # Use the list of containers
    display_output(results)

# Function to display the output in a new frame and save it to a file
def display_output(results):
    output_text = ""

    # Open the output file to save the results in the specified format
    with open("output.txt", "w") as output_file:
        for idx, result in enumerate(results):
            # Get the correct container details
            container_name = container_details_list[idx][0]
            container_dimensions = container_details_list[idx][1]
            container_volume = container_dimensions[0] * container_dimensions[1] * container_dimensions[2]  # L * W * H
            used_volume = sum(float(item['dimensions'][0]) * float(item['dimensions'][1]) * float(item['dimensions'][2]) for item in result['fitted_items'])
            remaining_volume = container_volume - used_volume

            # Add details to the output text
            output_text += f"Bin: {container_name}\n"
            output_text += f"Total Volume: {container_volume} cm^3\n"
            output_text += f"Space Utilization: {result['space_utilization']}%\n"
            output_text += f"Remaining Volume: {remaining_volume} cm^3\n"
            output_text += f"Gravity Distribution: {result['gravity_distribution']}\n\n"

            output_text += "FITTED ITEMS:\n"
            for item in result['fitted_items']:
                output_text += f"Part No: {item['partno']}, Dimensions: ({item['dimensions'][0]} * {item['dimensions'][1]} * {item['dimensions'][2]}), Weight: {item['weight']}kg\n"

            # Adding cushioning material output for fitted items
            output_text += "\nCUSHIONING MATERIALS USED:\n"
            for item, material in result.get('cushioning_materials', []):
                output_text += f"Item {item} is supported by {material}\n"

            
            output_text += "\nUNFITTED ITEMS:\n"
            for item in result['unfitted_items']:
                output_text += f"Part No: {item['partno']}, Dimensions: ({item['dimensions'][0]} * {item['dimensions'][1]} * {item['dimensions'][2]}), Weight: {item['weight']}kg\n"

            output_text += "\n" + "-" * 50 + "\n"  # Separator for readability

            # Write the same details to the output file in the specified format
            output_file.write(f"Bin: {container_name}\n")
            output_file.write(f"Total Volume: {container_volume} cm^3\n")
            output_file.write(f"Space Utilization: {result['space_utilization']}%\n")
            output_file.write(f"Remaining Volume: {remaining_volume} cm^3\n")
            output_file.write(f"Gravity Distribution: {result['gravity_distribution']}\n\n")
            


            output_file.write("FITTED ITEMS:\n")
            for item in result['fitted_items']:
                output_file.write(f"Part No: {item['partno']}, Dimensions: ({item['dimensions'][0]} * {item['dimensions'][1]} * {item['dimensions'][2]}), Weight: {item['weight']}kg\n")

            
            # Output cushioning material data
            if 'cushioning_materials' in result:
                output_text += "\nCUSHIONING MATERIALS USED:\n"
                for cushioning in result['cushioning_materials']:
                    output_text += f"Item: {cushioning['item']} - Cushion Material: {cushioning['material']}\n"

            output_file.write("\nUNFITTED ITEMS:\n")
            for item in result['unfitted_items']:
                output_file.write(f"Part No: {item['partno']}, Dimensions: ({item['dimensions'][0]} * {item['dimensions'][1]} * {item['dimensions'][2]}), Weight: {item['weight']}kg\n")

            output_file.write("\n" + "-" * 50 + "\n")  # Separator for readability

    # Update the text widget with the results
    output_text_widget.config(state=tk.NORMAL)
    output_text_widget.delete("1.0", tk.END)
    output_text_widget.insert(tk.END, output_text)
    output_text_widget.config(state=tk.DISABLED)

    show_frame(output_frame)


# Function to show a specific frame
def show_frame(frame):
    frame.tkraise()

# Create the main window
root = tk.Tk()
root.title("Storage Optimization - 3D Parcels Placement")
root.geometry("600x600")

# Make the window full-screen for output display
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", True)

def end_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", end_fullscreen)

# Create frames for different sections
main_frame = tk.Frame(root)
parcel_frame = tk.Frame(root)
output_frame = tk.Frame(root)

for frame in (main_frame, parcel_frame, output_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# -------------------- Main Page (Container Input Form) --------------------

# Dropdown label
dropdown_label = tk.Label(main_frame, text="Select Algorithm:", font=("Arial", 12))
dropdown_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky='ew')

# Dropdown for selecting algorithm
algo_combobox = ttk.Combobox(main_frame, values=["3D Parcels Placement"])
algo_combobox.grid(row=0, column=2, padx=10, pady=5, sticky='ew')

# Button to confirm selection
algo_button = tk.Button(main_frame, text="Select", command=select_algorithm, width=10)
algo_button.grid(row=0, column=3, padx=10, pady=5, sticky='ew')

# Label to display selected algorithm
selected_option_label = tk.Label(main_frame, text="Selected Algorithm: ", font=("Arial", 12), fg="blue")
selected_option_label.grid(row=1, column=0, columnspan=4, pady=10, sticky='ew')

# Label for input prompt
title_label = tk.Label(main_frame, text="Please Input Container Details (Positive Numbers):", font=("Arial", 12))
title_label.grid(row=2, column=0, columnspan=4, pady=10, sticky='ew')

# Number of Containers input
num_boxes_label = tk.Label(main_frame, text="Number of Containers:")
num_boxes_label.grid(row=3, column=0, padx=10, pady=5)
num_boxes_entry = tk.Entry(main_frame)
num_boxes_entry.grid(row=3, column=1, columnspan=3)

# Dimensions of the container (Length, Width, Height)
container_dim_label = tk.Label(main_frame, text="Container Dimensions (Length, Width, Height in cm):")
container_dim_label.grid(row=4, column=0, columnspan=4, pady=5)

container_length_label = tk.Label(main_frame, text="Length:")
container_length_label.grid(row=5, column=0)
container_length_entry = tk.Entry(main_frame, width=10)
container_length_entry.grid(row=5, column=1)

container_width_label = tk.Label(main_frame, text="Width:")
container_width_label.grid(row=6, column=0)
container_width_entry = tk.Entry(main_frame, width=10)
container_width_entry.grid(row=6, column=1)

container_height_label = tk.Label(main_frame, text="Height:")
container_height_label.grid(row=7, column=0)
container_height_entry = tk.Entry(main_frame, width=10)
container_height_entry.grid(row=7, column=1)

# Maximum weight capacity input
container_weight_label = tk.Label(main_frame, text="Maximum Weight Capacity (in kg):")
container_weight_label.grid(row=8, column=0)
container_max_weight_entry = tk.Entry(main_frame, width=10)
container_max_weight_entry.grid(row=8, column=1)

# Buttons
create_button = tk.Button(main_frame, text="Create Containers", state=tk.DISABLED, command=create_boxes, bg="green", fg="white", width=15)
create_button.grid(row=9, column=1, pady=20, columnspan=2)

clear_button = tk.Button(main_frame, text="Clear", command=lambda: clear_fields(), bg="yellow", fg="black", width=10)
clear_button.grid(row=9, column=3, pady=20)

# -------------------- Parcel Page (Parcel Input Form) --------------------

# Label for parcel input prompt
parcel_title_label = tk.Label(parcel_frame, text="Please Input Box Details:", font=("Arial", 12))
parcel_title_label.grid(row=0, column=0, columnspan=4, pady=10, sticky='ew')

# Number of parcels input
num_parcels_label = tk.Label(parcel_frame, text="Number of Parcels:")
num_parcels_label.grid(row=1, column=0, padx=10, pady=5)
num_parcels_entry = tk.Entry(parcel_frame)
num_parcels_entry.grid(row=1, column=1, columnspan=3)

# Dimensions Range for parcel (Low to High: Length, Width, Height)
parcel_dim_label = tk.Label(parcel_frame, text="Length, Width, Height Ranges (Low to High in cm):")
parcel_dim_label.grid(row=2, column=0, columnspan=4, pady=5)

# Length input fields
parcel_length_low_label = tk.Label(parcel_frame, text="Length (Low):")
parcel_length_low_label.grid(row=3, column=0)
parcel_length_low_entry = tk.Entry(parcel_frame, width=10)
parcel_length_low_entry.grid(row=3, column=1)

parcel_length_high_label = tk.Label(parcel_frame, text="Length (High):")
parcel_length_high_label.grid(row=3, column=2)
parcel_length_high_entry = tk.Entry(parcel_frame, width=10)
parcel_length_high_entry.grid(row=3, column=3)

# Width input fields (corrected)
parcel_width_low_label = tk.Label(parcel_frame, text="Width (Low):")
parcel_width_low_label.grid(row=4, column=0)
parcel_width_low_entry = tk.Entry(parcel_frame, width=10)
parcel_width_low_entry.grid(row=4, column=1)

parcel_width_high_label = tk.Label(parcel_frame, text="Width (High):")
parcel_width_high_label.grid(row=4, column=2)
parcel_width_high_entry = tk.Entry(parcel_frame, width=10)
parcel_width_high_entry.grid(row=4, column=3)

# Height input fields
parcel_height_low_label = tk.Label(parcel_frame, text="Height (Low):")
parcel_height_low_label.grid(row=5, column=0)
parcel_height_low_entry = tk.Entry(parcel_frame, width=10)
parcel_height_low_entry.grid(row=5, column=1)

parcel_height_high_label = tk.Label(parcel_frame, text="Height (High):")
parcel_height_high_label.grid(row=5, column=2)
parcel_height_high_entry = tk.Entry(parcel_frame, width=10)
parcel_height_high_entry.grid(row=5, column=3)

# Weight Range
parcel_weight_label = tk.Label(parcel_frame, text="Weight Range (Low to High in kg):")
parcel_weight_label.grid(row=6, column=0, columnspan=4, pady=5)

parcel_weight_low_entry = tk.Entry(parcel_frame, width=10)
parcel_weight_low_entry.grid(row=7, column=1)
parcel_weight_high_entry = tk.Entry(parcel_frame, width=10)
parcel_weight_high_entry.grid(row=7, column=2)

generate_random_parcels_button = tk.Button(parcel_frame,text="Generate Parcels",command=save_parcels,bg="orange",fg="white",width=20)
generate_random_parcels_button.grid(row=8, column=0, pady=20)

back_button = tk.Button(parcel_frame, text="Back", command=lambda: show_frame(main_frame), bg="red", fg="white", width=10)
back_button.grid(row=8, column=3, pady=20)

clear_button = tk.Button(parcel_frame, text="Clear", command=lambda: clear_fields(), bg="yellow", fg="black", width=10)
clear_button.grid(row=8, column=5, pady=20)


# -------------------- Manual Parcel Entry Section --------------------

# Manual parcel entry label
manual_entry_label = tk.Label(parcel_frame, text="Manual Parcel Entry", font=("Arial", 12))
manual_entry_label.grid(row=9, column=0, columnspan=4, pady=10, sticky='ew')

# Manual parcel entry fields
tk.Label(parcel_frame, text="Length (cm):").grid(row=10, column=0, padx=10, pady=5)
manual_length_entry = tk.Entry(parcel_frame)
manual_length_entry.grid(row=10, column=1, padx=10, pady=5)

tk.Label(parcel_frame, text="Width (cm):").grid(row=11, column=0, padx=10, pady=5)
manual_width_entry = tk.Entry(parcel_frame)
manual_width_entry.grid(row=11, column=1, padx=10, pady=5)

tk.Label(parcel_frame, text="Height (cm):").grid(row=12, column=0, padx=10, pady=5)
manual_height_entry = tk.Entry(parcel_frame)
manual_height_entry.grid(row=12, column=1, padx=10, pady=5)

tk.Label(parcel_frame, text="Weight (kg):").grid(row=13, column=0, padx=10, pady=5)
manual_weight_entry = tk.Entry(parcel_frame)
manual_weight_entry.grid(row=13, column=1, padx=10, pady=5)

# Button to add the manual parcel entry
add_manual_parcel_button = tk.Button(parcel_frame, text="Add Parcel", command=lambda: add_manual_parcel(
    manual_length_entry.get(), manual_width_entry.get(), manual_height_entry.get(), manual_weight_entry.get()), bg="blue", fg="white", width=15)
add_manual_parcel_button.grid(row=14, column=0, columnspan=2, pady=10)


# Buttons for parcel input
output_button = tk.Button(parcel_frame, text="Output", command=lambda: run_algorithm_and_show_results(), bg="black", fg="white", width=15)
output_button.grid(row=14, column=3, pady=20)


# -------------------- Output Page (Enhanced Full-Screen Results Display) --------------------

# Create a scrollable text widget for displaying the output
output_scrollbar = tk.Scrollbar(output_frame)
output_text_widget = tk.Text(output_frame, wrap="word", height=25, width=60, yscrollcommand=output_scrollbar.set)
output_scrollbar.config(command=output_text_widget.yview)

output_text_widget.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
output_scrollbar.grid(row=0, column=4, sticky="ns")

output_text_widget.config(state=tk.DISABLED)

# Back button to return to the main frame
output_back_button = tk.Button(output_frame, text="Back", command=lambda: show_frame(main_frame), bg="red", fg="white", width=10)
output_back_button.grid(row=1, column=3, pady=10)

# Initially show main frame
show_frame(main_frame)

# Run the main loop
root.mainloop()