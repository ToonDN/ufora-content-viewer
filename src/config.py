# Which browser to check for authentication cookies
browsers = ("firefox",)


# Map specific orgunitids to specific urls
CUSTOM_VTK_URL_MAP = {
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

