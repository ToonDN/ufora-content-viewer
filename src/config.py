# The directory where to output the generated html and downloaded files (the downloads will always be placed in a download subfolder)
export_directory = "/home/toon/ufora_content_viewer_export"

# Which browser to check for authentication cookies
browsers = ("firefox",)

# The courses that are loaded
courses = (
	448074, # Multimediatechnieken
	443572, # Vakoverschrijdend
	439934, # Formele systeemmodellerings voor software
	450929, # Automatenleer
	450222, # Softwareontwikkeling
    442214, # Information theory
    442175, # Recommender systems
    440412, # Big data science
)

# Map specific orgunitids to specific urls
custom_vtk_url_map = {
        228918: "https://vtk.ugent.be/wiki/ingenieursproject-ii-computerwetenschappen/",
        228782: "https://vtk.ugent.be/wiki/algemene-scheikunde/",
        228811: "https://vtk.ugent.be/wiki/wiskundige-analyse-iii/",
        442195: "https://vtk.ugent.be/wiki/wachtlijnanalyse-en-simulatie/",
        442214: "https://vtk.ugent.be/wiki/informatietheorie/",
        440412: "https://vtk.ugent.be/wiki/big_data_science/",
    }
    
# Local storage mananging 
# Since all data is stored in the browsers local storage this can be used to backup all data
local_storage_path = "/home/toon/.mozilla/firefox/qylnyonf.default-release/webappsstore.sqlite"
local_storage_table = "webappsstore2"

