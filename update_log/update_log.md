# Index.html
## icon
Resolve the problem where the icon is missing when users visit the webpage.
## permission
Add a feature to decide which permission to present.
## Mydriatic agent
Adjust options in Mydriatic agent to fit model on AWS
## Upload button
Adjust code execution processs of upload button to check more form state before form uploading.
## Site selector
Add warning message to notify user when user trying to upload null value.  
Add a hint message to notify the user whether the data is being stored in the cloud or not.
## Height input
Add a validation mechanism to ensure that input data is correct.  
Numbers must have a maximum of 3 digits for the integer part and 3 digits for the decimal part.
## Date of visit
Add a limitation to prevent the user from choosing a date that is after today.
## Date of birth
Add a limitation to ensure that the user cannot choose a date that is at least 3 years ago.
## Gender selection
Add a verification mechanism to prevent gender recording in different language.
## Fetal status
Add a verification mechanism to prevent Fetal status recording in different language.
## Week input
Add a validation mechanism to ensure that input data is correct.
Numbers must be within the range of 0 to 42.
## Day input
Add a validation mechanism to ensure that input data is correct.  
Numbers must be within the range of 0 to 6.
## Degree of myopia with father
Add a validation mechanism to ensure that input data is correct.  
Numbers must be less than or equal to -5.  
Numbers must have a maximum of 3 digits for the integer part and 2 digits for the decimal part.
## Degree of myopia with mother
Add a validation mechanism to ensure that input data is correct.  
Numbers must be less than or equal to -5.  
Numbers must have a maximum of 3 digits for the integer part and 2 digits for the decimal part.
## OD BCVA
Add the maximum value and minimum value at the edge of the range.  
To prevent misunderstanding, hide this options.  
Hide the option "glasses" wtih.  
Ensure that the value is null before the user selects the required value. If the value is null, set the default value to 1 to ensure that OD BCVA is not null.
## OS BCVA
Add the maximum value and minimum value at the edge of the range.   
To prevent misunderstanding, hide this options.  
Hide the option "glasses" wtih.  
Ensure that the value is null before the user selects the required value. If the value is null, set the default value to 1 to ensure that OS BCVA is not null.
## OD SPH
Add the maximum value and minimum value at the edge of the range.  
Make sure the value is null before the user selects the required value.
## OS SPH
Add the maximum value and minimum value at the edge of the range.  
Make sure the value is null before the user selects the required value.
## OD CYL
Add the maximum value and minimum value at the edge of the range.  
Make sure the value is null before the user selects the required value.
## OS CYL
Add the maximum value and minimum value at the edge of the range.  
Make sure the value is null before the user selects the required value.
## OD Axis
Add warning message to notify user when user trying to upload null value.
## OS Axis
Add warning message to notify user when user trying to upload null value.
## OD AL
Add warning message to notify user when user trying to upload null value.
## OS AL
Add warning message to notify user when user trying to upload null value.
## Treartment
Add a detection mechanism to monitor the AWS state, preventing the AWS serverless from entering sleep mode.
## Axial length risk assessment
Add a detection mechanism to monitor the AWS state, preventing the AWS serverless from entering sleep mode.
## Spherical diopter risk assessment
Add a detection mechanism to monitor the AWS state, preventing the AWS serverless from entering sleep mode.
## Upload
Add a detection mechanism to monitor the form state.
# Report.html
## icon
Resolve the problem where the icon is missing when users visit the webpage.
## py-config
Include the necessary packages and fonts for various languages.
## Scss
Add some style classes for the print feature..
## BCVA
To prevent misunderstanding, hide this options.
## Gender
Resolve the issue of gender not displaying correctly in different languages.
## Age
Resolve the issue of age not displaying correctly in different languages.
## References
Add References in different language.
## Display of values
Adjust display of values when value is out of range.
## Treatment
Adjust the display options on the 'report.html'.
## Print
Add a print feature with button below.  
Adjust the font size, field height, and picture size on the print page using the selected print SCSS style.
# plot.py
## dataplot.pkl
Update new data for risk assessment.
## Font
Load target font when user language is traditional chinese or simple chinese.  
The font will allow the plot to display Chinese characters.
## Moving average(function)
Add a new function for calculating the moving average to generate a color block chart for risk assessment.
## Plot(function)
Incorporate a smoothing feature to create a smoother appearance for the color block chart.
## Titles (function)
Enhance the title's performance by adjusting the font based on the selected language.
## Treatment recommendations
Display the treatment recommendations based on the selected language, gender, eyeside, and risk classification.
## Create a trend chart
Replace '.' with '⯁' when displaying latest records.  
Replace '.' with '★' when displaying future records which is generating by our training model.  
Create a blue and red color band block chart with confidence intervals which is generating by our training model to display the positive range.  
Make all marks and color block chart display on legent.  
Add dataset version to legend.
# Table.py
## dataplot.pkl
Load this pkl for showing future trend data in table.
## Font
Load target font when user language is traditional chinese or simple chinese.  
The font will allow the table to display Chinese characters.
## Table
Add '⯁' to represent latest records on the plot.  
Add future records which is generating by our training model to table.  
Add '★' to represent future records which is generating by our training model on the plot.  
Add '●' to represent past records on the plot.  
Adjust performance when value is bigger than 30 or less than 20.  
Add units to the table based on the selected language.  
Replace the old performance style with a new style to enhance the clarity of the table's display.