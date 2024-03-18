import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly, output_widget, render_widget
from shiny import render, App
import palmerpenguins # import the Palmer Penguin dataset
import seaborn as sns


# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Gagnon-Vos Penguin Data", fillable=True)

# Add a Shiny UI sidebar for user interaction

with ui.sidebar(open = "open"):
    ui.h2("Sidebar")


# Use ui.input_selectize() to create a dropdown input to choose a column
    
    ui.input_selectize("selectized_attribute", "Select Attribute", ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

# Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins

    ui.input_numeric("plotly_bin_count", "Bin Count", 1, min=1, max=20)

# Use ui.input_slider() to create a slider input for the number of Seaborn bins

    ui.input_slider("seaborn_bin_count", "Bin Count", 0, 100, 50)

# Use ui.input_checkbox_group() to create a checkbox group input to filter the species

    ui.input_checkbox_group("selected_species_list", "Species", ["Adelie", "Gentoo", "Chinstrap"], selected=["Adelie"], inline=False)

# Use ui.hr() to add a horizontal rule to the sidebar

    ui.hr()

# Use ui.a() to add a hyperlink to the sidebar

    ui.a("Github", href="https://github.com/lauravos/cintel-02-data", target="_blank")


#DataTable
with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Data Table"):
        @render.data_frame  
        def penguins_dataTable():
            return render.DataTable(penguins_df)  

#DataGrid
    with ui.nav_panel("Data Grid"):
        ui.h2("Palmer Penguins")
        @render.data_frame  
        def penguins_dataGrid():
            return render.DataGrid(penguins_df)  


#Plotly Histogram
with ui.accordion(id="acc", open="closed"):
    with ui.accordion_panel("Plotly Histogram"):   
        ui.input_slider("n", "Number of bins", 1, 100, 20)

        @render_widget  
        def plotly():  
            scatterplot = px.histogram(
                data_frame=penguins_df,
                x="body_mass_g",
                nbins=input.n(),
            ).update_layout(
                title={"text": "Penguin Mass", "x": 0.5},
                yaxis_title="Count",
                xaxis_title="Body Mass (g)"
            )

            return scatterplot  


#Seaborn Histogram
    with ui.accordion_panel("Seaborn Histogram"):
        ui.input_slider("m", "Number of bins", 1, 100, 25)

        @render.plot(alt="A Seaborn histogram on penguin body mass in grams.")  
        def plotHistogram():  
            ax = sns.histplot(data=penguins_df, x="body_mass_g", bins=input.m())  
            ax.set_title("Palmer Penguins")
            ax.set_xlabel("Mass (g)")
            ax.set_ylabel("Count")
            return ax  


#Plotly Scatterplot

with ui.card(full_screen=True):

    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        # Create a Plotly scatterplot using Plotly Express
        # Call px.scatter() function
        # Pass in six arguments:
        fig = px.scatter(penguins_df, x="bill_length_mm", y="flipper_length_mm", 
                         color="species", title="Scatterplot",labels={"bill_length_mm": "Bill Length (mm)",
                         "flipper_length_mm": "Flipper Length (mm)"})
        return fig
