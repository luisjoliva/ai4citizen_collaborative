# ai4citizen_collaborative

The system requires using the Team Formation docker container. It can be found on this URL: https://www.ai4eu.eu/resource/edu2comapi along a document explaining how to install it, turn it on and consume it.
Download the files, decompress them and follow the instructions of the abovementioned document.
Using this command, you can turn on the container:

docker run -p 5000:5000 --name teamformation teamformation:latest

It launches the container using the latest image of teamformation, connects its port 5000 to localhost:5000, and names it accordingly.
The API is documented in the file that can be found in previous URL. The Docker also allows you to access the swagger file, which describes the API as well. Nevertheless, contrary to what the documentation says, the swagger is accessed through this URL: http://localhost:5000/AI4U/teamformationui/
There you can play around the API and understand how it works.

Besides this, the code provided requires a specific Python library, ‘requests’, which can be installed using pip:

pip3 install requests

You can now execute the code for interactions. It is divided in three main files:
-	Main.py
-	Interaction.py
-	Test/test_interaction.py
There is also a /resources folder which contains test data as well as a /full subfolder, which contains a more realistic/real data, with a higher amount of data.

The main file contains functions that consume the different API endpoints, using test data (contained in /resources folder). The test data was provided by teamformation developers:
	
-	get_ontology/dataset_list: to retrieve what ontology and dataset is loaded in the algorithm
-	post_ontology/dataset: to provide a new ontology and dataset to be loaded in the algorithm
-	call_uploading_data: provides all the files as a post request and retrieves the response. This is the main way to interact with the algorithm, uploading specific students, projects and preferences.
-	Call_with_loaded: although this is supposed to use whatever is loaded in the container, it posed some difficulties since it seemed to not work properly with that default data

There are also some auxiliary functions, to build the URL to consume the endpoints, store the results or generate requests.
 
The interaction file contains, right now, the most basic kind of interaction: people who have accepted the assignment. For the time being that means that only if all the people assigned to a project accept it, we can consider it as solved. If at least one has not accepted it, we do not consider it as solved. If solved, we remove that project from the state of the world and we should then repeat the algorithm with the remaining non-solved assignments as well as removing the assigned students.

Finally, the /test/test_interaction file contains a test which tries to simulate interaction cycles, that is, we have an initial state of the world with assignments, we receive some feedback, process the interactions and repeat the execution of the teamformation algorithm to simulate another round, and return the new state of the world, with (maybe) a different assignment obtained from the non-assigned students and remaining projects. Ideally, we should use the Mock library to avoid having to use the Docker container and decoupling both systems (Docker and the code for interactions).

Note: the datasets under the full subfolder has a different structure from the test data. If you try to use it with the Docker container, it will not work. Maybe there is a newer version of the algorithm which has not been published in AI4EU (at least, at the time this document is being written).
Note2: There is a file called team_response.json which could be used to avoid having to use the Docker container, at least for basic tests. It contains an initial project-student assignment.
