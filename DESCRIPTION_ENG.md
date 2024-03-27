## Project SPORT PORTAL

### Project:
Sports Portal is a platform with monitoring of sports results and training and education programs, where any number of companies and their departments, as well as coaches, can be hosted.


### Idea
I have an acquaintance who has her own weight loss marathon, and I also have acquaintances in another country who also train groups for weight loss and sports.


### Uniqueness:
There are many commercial platforms with products, but I have not come across a sports oriented platform with simultaneous monitoring and training programs


### Objective
To make a full-fledged project that could potentially have a commercial application. To apply the knowledge gained in practice. To demonstrate the knowledge that was passed on to us by our instructor on the course.


### Execution:
When designing the project structure and database, I considered the real requirements (as if it were commercial). Before starting the development, I clarified and analyzed what data is important for the real work and trainings

### Stack:
Python, Django, Django Rest Framework, Swagger, Redoc, Faker, PIL


### Implemented:
- Custom managers and additional users (reworked and replaced cumbersome methods for creating users). 

- Through custom manager I have 4 kinds of users created: superuser, administrator, trainer and client.

- I made custom poly-authentication by email or username or nickname (based on github example).

- For privacy, I separated the authentication and user models:
- Custom User model - for authentication
- Custom Administrator, Coach, Client models for user categories.

- Following the example of accounting or financial programs, each model has a creator field as a record creator or editor.

- Custom permission classes for SuperUsers, Administrators, Coaches, Clients, and additional IsActive and IsVerified permission classes have been created

- All views can receive different combinations of access permissions from the list of standard or custom permissions.

- Only superuser has the right to hard delete a record

Restricted the ability to create users in the admin area. Superuser can create any users. Administrator all but superuser. Coach and client can not create users.

In the admin, depending on the user category, the availability of some fields is disabled

In admin overridden methods to get filtered values from relational model for select fields

The creator field is limited to the current user only.

- Everything is in English. Applied verbose_name and django utility translations.gettext-lazy, which automatically tries to do the translation depending on the user's geo-location

- Clear project structure in accordance with Django project architecture

- All text and information constants are placed in a separate application 'messages'.

- All parameters of settings by sizes of figures, permissible values of fields are placed in separate modules of applications 'settings'.

- All auxiliary utility functions have been moved to a separate application 'utils'.

- Validators are placed in separate application modules 'validators'.

- All variables without abbreviations in accordance with PEP requirements for better readability and understanding.


### Issues that arose and solutions found:
- Cyclic import error on one-to-one communication. To solve, used literals instead of importing "app.<model>"

- Creator field from the model itself. Solution - using "self" literal

- Bug django with accumulation of image files was solved by using signals in which I validate, modify or delete unnecessary image files, so that there is one record - one image, if the record is deleted, then the image too

- Naming a file containing the id number of an object that does not yet exist when the file is saved was also solved using signals with swapping image files and assigning a new name

- Used signals to validate the file size and reduce it, to avoid server overflow or deliberately sending a large file size

- Standard admin panel did not work properly with custom user (password was not validated for repetition, password was not hashed when creating and updating, password was not hidden behind characters when entering), so I made custom admin panel and bound custom form, added intermediate field password2 for validation of repetition.

- Due to many many-to-many in django it was impossible to make a composite (composite primary key (group+client), so I created a custom intermediate table.

In admin, many-to-many fields do not work with custom intermediate tables. The solution is to use admin.TabularInline (embed a table with row-by-row view for the intermediate model in the main admin).

- Django migrations did not always correctly perform migrations for models with many-to-many and custom table, migrations created tables and immediately complained that they could not overwrite the table because it already exists. The solution is to manually do migrations of each table in order by relational relationship level.

- Django migrations did not always work correctly, could save some field or parameter in the migration and then because of this refused to work. The solution is to adjust some parameters of the migration file

- Bug Django when a Boolean field returns None from serializer if the field was not flagged (not selected), as a result the field was not saved, because it was not in the list of unselected fields. The solution is to assign False instead of None to the attribute during validation, then the view sees the changes and saves correctly

- Bug Django. In relational fields one-to-many parameter slug_field can normally reflect fields other than id only if read_only=True, otherwise it accepts only id or tries to write string value (__str__) to id. Solution - to reflect another field, you need to override the to_represent method. 

- Bug Django.In relational many-to-many fields, the slug_field parameter can only accept id or tries to write a string value (__str__) to the id. Solution - the field cannot be replaced by to_represent, you can only assign another additional field to display with a different name.

- Bug Django. When saving numeric fields, if the field is not proavlidized, it is simply skipped and nothing is written to the database. Exception is not called, the user does not know that an empty value was written instead of his data. The solution is to define a CharField with the same field name in the serializer, get a string value, convert to a number in the validate() method, validate and return the correct value to attrs, and if it is impossible, then a response with a code and an error message


### Flexibility and extensibility:
- at the moment it is a pure back-end with information about personal data in the process of training and data about customer payments with binding to groups (admin, urls, validation, views)

- in the future you can easily expand to any training courses and trainings (not only sports)

- the project is pre-customized for different geo-locations, all field names and messages are displayed in separate files for quick translation and adaptation of the project

- connection of an additional API as a separate service, where trainers, coaches can place training programs and give access to clients depending on their statuses and payments

- Connection of API of Telegram bot or other active messenger in a particular country

- API connection of a mobile application

- the project is pre-customized for different geo-locations, all field names and messages are displayed in separate files for quick translation and adaptation of the project

- connect front end as a separate service, on JS or Django templates and forms

- connect parsing from any site with information about calories, as well as exercises

- translate the project into Fast API


### Additional analytics (front):
- further analytics (graphs and charts of current performance) can be outputted

- output of trend lines showing the future dynamics of sports indicators

- Multivariate analysis of variance, e.g:
- the relationship between the amount of money paid and training results
- correlation between the level of emotional state and training results
- other metrics that could be of interest to both companies and users to be commercially attractive and give users a unique offer that other platforms do not have


### Issues that need to be addressed:
- PIL won't let me open an image file in "rb" mode, but under the hood it checks and swears that the mode should be "r" only
