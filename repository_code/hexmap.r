################################################################################
# Generate a hexmap of the US, with states coloured by some binary status
#
# Dependency (all in this repository):
#	merge_on_statecodes.csv, a spreadsheet mapping state names to IDs
#	statuses.csv, a spreadsheet specifying the status of each state
#	hexmap.Rdata
#
# written by sbaltz at mit,
#	late 2022,
#	based on code that I think was by john curiel
################################################################################
library(sp)
library(tidyverse)
library(broom)
library(rgeos)
library(rgdal)

################################################################################
# Global variables
################################################################################
WORK_DIR <- "/home/sbaltz/documents/precincts/2022-precincts/repository-code"
STATE_CODE_PATH <- "/home/sbaltz/documents/precincts/2022-precincts/help-files/"

setwd(WORK_DIR)
stateCodeFname <- paste0(STATE_CODE_PATH,"merge_on_statecodes.csv")


################################################################################
# Read data and initialize the map
################################################################################
hexmap <- readRDS("hexmap.Rdata")
hexmap <- readRDS("hexmap.Rdata")
state_codes <- read.csv(stateCodeFname)
statuses <- read.csv("statuses.csv")
state_codes <- merge(state_codes, statuses, by = "state")
hexmap <- merge(hexmap, state_codes, by.x="iso3166_2", by.y="state_po")

#Define the plot colours
hexmap$colour[hexmap$status=="done"] <- "#ff00ff"
hexmap$colour[hexmap$status=="semi"] <- "#ddaadd"
hexmap$colour[hexmap$status=="not started"] <- "#cAcAcA"
colours <- c()
for (c in hexmap$colour) {
  colours <- append(colours, rep(c,7))
}

# Calculate the centroid of each hexagon to add the label:
centers <- cbind.data.frame(
		 data.frame(gCentroid(hexmap, byid=TRUE),
		 id=hexmap@data$iso3166_2)
			   )

################################################################################
# Plot the map
################################################################################
theCaption <- paste0("Source: MIT Election Data and Science Lab\n",
		     "github.com/MEDSL/2022-elections-official"
		    )
hexplot <- ggplot() +
  geom_polygon(data = hexmap, aes( x = long, y = lat, group = group),
               fill=colours, color="white") +
  geom_text(data=centers, aes(x=x, y=y, label=id)) +
  theme_void() +
  coord_map() +
  theme_void() +
  labs(title="Progress of 2022 precinct data",
        caption = theCaption) +  
  theme(text=element_text(family="Styrene B"), 
        title = element_text(size = rel(1.2)),
        legend.direction = "horizontal",
        legend.position = "bottom",
        plot.caption = element_text(hjust=0))

ggsave("precinct_progress_map.png", plot = hexplot, scale = 1,
       width = 9, height = 6, units = c("in"), dpi = 600, bg='white')
