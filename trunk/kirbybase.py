"""Contains classes for a plain-text, client-server dbms.

Classes:
    KirbyBase - database class
    KBError - exceptions

Example:
    from db import *

    db = KirbyBase()
    db.create('plane.tbl', ['name:str', 'country:str', 'speed:int',
     'range:int'])
    db.insert('plane.tbl', ['P-51', 'USA', 403, 1201])
    db.insert('plane.tbl', ['P-38', 'USA', 377, 999])
    db.select('plane.tbl', ['country', 'speed'], ['USA', '>400'])
    db.update('plane.tbl', ['country'], ['USA'], ['United States'],
     ['country'])
    db.delete('plane.tbl', ['speed'], ['<400'])
    db.close()

Author:
    Jamey Cribbs -- jcribbs@twmi.rr.com
    www.netpromi.com

History:
    2003-04-08:  Version 1.0 released.
    2003-04-15:  Version 1.01 released.
        -Added getFieldNames method.
        -Added getFieldTypes method.
        -Added drop method.
        -Added check for existing file in create method.
        -Improved documentation.
    2003-07-16:  Version 1.02 released.
        -KirbyBase now uses distutils for installation.
        -Fixed bug in createTable where field list was getting modified.
        -Fixed bug in insert where values list was getting modified.
        -Added the ability to use special characters in table data such
         as \r, \n, \032, and |.
        -Changed the name of all private methods to start with two
         underscores, thereby following recommended naming conventions.
        -Improved documentation.
        -Added licensing information.
    2003-08-14:  Version 1.3 released.
        -Added len method.
        -Fixed bug in validateMatchCriteria where script was not
         restricting other match criteria if already attempting to match
         by recno.
        -Fixed bug in validateMatchCriteria where script was not checking
         to see if pattern argument was an integer when attempting to
         match by recno.
        -Added ability to pass field values to update and insert using a
         dictionary.
        -Added ability to specify field to sort on and sort direction for
        -the results of a select.
        -Changed the way field types are handled internally.  Instead of
         treating them as strings (which is how they are stored) and
         having to constantly 'eval' them to get the type, I decided to
         work with them in their 'native' format.  This should not change
         any of the api or interfaces, EXCEPT for the getFieldTypes
         method, which now returns a list of types, instead of a list of
         strings.  I hope this doesn't screw anyone's programs up.
        -Corrected version number to conform to guidelines in distutils
         documentation.
    2003-08-27:  Version 1.4 released.
        -Added two new database field types:  datetime.date and
         datetime.datetime.  They are stored as strings, but are input and
         output as instances of datetime.date and datetime.datetime
         respectively.  
        -Made a few internal optimizations when running queries that have
         resulted in a 15-20% speed increase when doing large queries or
         updates.
        -Changed the name of all private methods from starting with two
         underscores to starting with one underscore based on a discussion
         in comp.lang.python as to how to properly name private variables.
    2003-09-02:  Version 1.5 released.
        -Changed the way queries are handled internally.  Instead of doing
         an eval to do numeric and datetime comparisons, I changed it to do
         the actual comparison itself.  This resulted in a 40% speed 
         increase on large queries that do comparison expressions.
        -Changed how data is passed between the server and the client in
         client/server mode.  I now use cPickle instead of repr and eval.
         This resulted in an approximately 40% speed increase in 
         client/server operations.
    2004-06-10:  Version 1.5.1 released.
        -Added a new database field type:  boolean.
        -Fixed a bug where KirbyBase was trying to convert an empty table
         field (i.e. '') back into it's native format such as int or float
         and raising an Exception.  Now, if a table field is empty, I just
         append it to the result record as is and dont' try to convert it. 
        -getMatches method will now split each database record only up to
         the number of fields required to satisfy the query.  This should
         save a little query time on large databases with many fields.
        -Added ability to have the getMatches method match string fields
         based on string equality rather than regular expressions.  
    2004-06-22:  Version 1.6 released.
        -On numeric comparisons, you can now specify negative numbers.
        -Fixed a bug where program would crash if you had a space between
         the comparison operator and the number in numeric comparisons in
         select statement.
        -You can select all records by specifying that you want to match
         'recno' against '*'.  
        -Got rid of the last eval in the code.    
        -Modest speed improvement by checking for strings that need to be
         encoded first insteading of just encoding all strings.
        -Added a compatibility layer for declaring field types when 
         creating a table.  If you use the new compatible field types when
         creating a table, you can use the table either from the Python or
         Ruby version of KirbyBase without having to change anything. 
        -Changed the record-counter and deleted-records-counter in the
         header record of the table to be zero padded instead of spaces
         padded. 
"""
import re
import socket
import os.path
import time
import datetime
import cPickle

#--------------------------------------------------------------------------
# KirbyBase Class
#--------------------------------------------------------------------------
class KirbyBase:
    """Database Management System.

    Public Methods:
        __init__      - Create an instance of database.
        close         - Close database.
        create        - Create a table.
        insert        - Insert a record into a table.
        update        - Update a table.
        delete        - Delete record(s) from a table.
        select        - select record(s) from a table.
        pack          - remove deleted records from a table.
        drop          - Remove a table.
        getFieldNames - Get a list of a table's field names.
        getFieldTypes - Get a list of a table's field types.
        len           - Total number of records in table.
    """

    #----------------------------------------------------------------------
    # PUBLIC METHODS
    #----------------------------------------------------------------------

    #----------------------------------------------------------------------
    # init
    #----------------------------------------------------------------------
    def __init__(self, type='local', host=None, port=None):
        """Create an instance of the database and return a reference to it.

        Keyword Arguments:
            type - Connection type: local(default), client, or server.
            host - IP address of server to connect to, if connection type
                   is client.
            port - Port number of server to connect to, if connection type
                   is client.
        """
        self.connect_type = type

        # Regular expression used to determine if field needs to be
        # encoded.
        self.encodeRegExp = re.compile(r'\n|\r|\032|\|')

        # Regular expression used to determine if field needs to be
        # un-encoded.
        self.unencodeRegExp = re.compile(
         r'&linefeed;|&carriage_return;|&substitute;|&pipe;')

        # If connecting as client, open a socket connection with server.
        if self.connect_type == 'client':
            self.dbSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.dbSock.connect((host, port))

    #----------------------------------------------------------------------
    # close
    #----------------------------------------------------------------------
    def close(self):
        """Close connection to database server.
        """
        if self.connect_type == 'client':
            self.dbSock.close()

    #----------------------------------------------------------------------
    # create
    #----------------------------------------------------------------------
    def create(self, name, fields):
        """Create a new table and return True on success.

        Arguments:
            name   - physical filename, including path, that will hold
                     table.
            fields - list holding strings made up of multiple fieldname,
                     fieldtype pairs (i.e. ['plane:str','speed:int']).
                     Valid fieldtypes are: str, int, float, datetime.date,
                     datetime.datetime, bool or, for compatibility with 
                     the Ruby version of KirbyBase use String, Integer,
                     Float, Date, DateTime, and Boolean.

        Returns True if no exceptions are raised.
        """
        # If running as a client, then send the command to the server for
        # it to execute.
        if self.connect_type == 'client':
            return self._sendSocket("db.create('%s',%s)" %(name,fields))

        # Check to see if file already exists.
        if os.path.exists(name):
            raise KBError(name + ' already exists!')

        # Validate field types. Integer, String, Float, Date, DateTime, and
        # Boolean types are compatible between the Ruby and Python versions
        # of KirbyBase.
        for x in [y.split(':')[1] for y in fields]:
            if x not in ['int', 'Integer', 'str', 'String', 'float', 
             'Float', 'datetime.date', 'Date', 'datetime.datetime',
             'DateTime', 'bool', 'Boolean']:
                raise KBError('Invalid field type: ' + x)

        # Make copy of fields list so that value passed in is not changed.
        header_rec = list(fields)

        # Insert recno field, delete counter, and recno counter into
        # header record.
        header_rec.insert(0, 'recno:int')
        header_rec.insert(0, '000000')
        header_rec.insert(0, '000000')

        # Open the table in write mode since we are creating it new, write
        # the header record to it and close it.
        fptr = self._openTable(name, 'w')
        fptr.write('|'.join(header_rec) + '\n')
        self._closeTable(fptr)

        # Return success.
        return True

    #----------------------------------------------------------------------
    # insert
    #----------------------------------------------------------------------
    def insert(self, name, values):
        """Insert a new record into table, return unique record number.

        Arguments:
            name   - physical file name, including path, that holds table.
            values - list or dictionary containing field values of new
                     record.

        Returns unique record number assigned to new record when it is
        created.
        """
        # If running as a client, then send the command to the server for
        # it to execute.
        if self.connect_type == 'client':
            return self._sendSocket("db.insert('%s',%s)" %(name,values))

        # Open the table.
        fptr = self._openTable(name, 'r+')

        # Update the instance variables holding table header info
        self._updateHeaderVars(fptr)

        # If values is a dictionary, we are going to convert it into a
        # list.  That way, we can use the same validation and updating
        # routines regardless of whether the user passed in a dictionary
        # or a list.
        if isinstance(values, dict):
            record = []
            for field_name in self.field_names[1:]:
                # If the values dictionary has a key corresponding to
                # the field name of the table, append the dictionary
                # value to the table record.
                if field_name in values:
                    record.append(values[field_name])
                else:
                    # If the values dictionary does not have a key
                    # corresponding to the field name of the table, append
                    # a ''.
                    record.append('')
        else:
            # If values is a list, make a copy of it so that it is no
            # pointing to a list in the calling scope.  That way, when
            # we insert the recno below into values, we will only be
            # modifying our local copy of values.
            record = list(values)

        # Check input fields to make sure they are valid.
        self._validateUpdateCriteria(record, self.field_names[1:])

        # Get a new record number.
        rec_no = self._incrRecnoCounter(fptr)

        # Add record number to front of record.
        record.insert(0, rec_no)

        # Append the new record to the end of the table and close the
        # table.  Run each field through encoder to take care of special
        # characters.
        self._writeRecord(fptr, 'end', '|'.join(map(self._encodeString,
         [str(item) for item in record])))
        self._closeTable(fptr)

        # Return the unique record number created for this new record.
        return rec_no

    #----------------------------------------------------------------------
    # update
    #----------------------------------------------------------------------
    def update(self, name, fields, searchData, updates, filter=None, 
     useRegExp=True):
        """Update record(s) in table, return number of records updated.

        Arguments:
            name       - physical file name, including path, that holds
                         table.
            fields     - list containing names of fields to search on. If 
                         any of the items in this list is 'recno', then the
                         table will be searched by the recno field only and
                         will update, at most, one record, since recno is 
                         the system generated primary key.
            searchData - list containing actual data to search on.  Each 
                         item in list corresponds to item in the 'fields' 
                         list.
            updates    - list or dictionary containing actual data to put
                         into table field.  If it is a list and 'filter' 
                         list is empty or equal to None, then updates list
                         must have a value for each field in table record.
            filter     - list containing names of fields to update.  Each
                         item in list corresponds to item in the 'updates'
                         list.  If 'filter' list is empty or equal to None,
                         then 'updates' list must have an item for each 
                         field in table record, excepting the recno field.

        Returns integer specifying number of records that were updated.

        Example:
            db.update('plane.tbl',['country','speed'],['USA','>400'],
             [1230],['range'])

            This will search for any plane from the USA with a speed
            greater than 400mph and update it's range to 1230 miles.
        """
        # If running as a client, then send the command to the server for
        # it to execute.
        if self.connect_type == 'client':
            return self._sendSocket("db.update('%s',%s,%s,%s,%s,%s)" 
             %(name, fields, searchData, updates, filter, useRegExp))

        # Make copy of searchData list so that value passed in is not 
        # changed if I edit it in validateMatchCriteria.
        patterns = list(searchData)

        # Open the table.
        fptr = self._openTable(name, 'r+')

        # Update the instance variables holding table header info.
        self._updateHeaderVars(fptr)

        # If no update filter fields were specified, that means user wants
        # to update all field in record, so we set the filter list equal
        # to the list of field names of table, excluding the recno field,
        # since user is not allowed to update recno field.
        if filter:
            # If updates is a dictionary, user cannot specify a filter,
            # because the keys of the dictionary will function as the
            # filter.
            if isinstance(updates, dict):
                raise KBError('Cannot specify filter when updates is a ' +
                 'dictionary.')
        else:
            # If updates is a dictionary, create an empty filter list.  We
            # will fill this with the keys of the dictionary below.
            if isinstance(updates, dict):
                filter = []
            else:
                # Otherwise, if updates is a list and no update filter
                # fields were specified, that means user wants to update
                # all fields in record, so we set the filter list equal
                # to the list of field names of table, excluding the recno
                # field, since user is not allowed to update recno field.
                filter = self.field_names[1:]

        # If updates is a dictionary, we are going to convert it into an
        # updates list and a filters list.  This will allow us to use the
        # same routines for validation and updating, regardless of whether
        # the user passed in a dictionary or a list.
        if isinstance(updates, dict):
            tempUpdates = []
            for key,value in updates.items():
                tempUpdates.append(value)
                filter.append(key)
            updates = tempUpdates

        try:
            # Check input arguments to make sure they are valid.
            self._validateMatchCriteria(fields, patterns)
            self._validateUpdateCriteria(updates, filter)
        except KBError:
            # If something didn't check out, close the table and re-raise
            # the error.
            fptr.close()
            raise

        # Search the table and populate the match list.
        match_list = self._getMatches(fptr, fields, patterns, useRegExp)

        # If matches were found, update them.
        if len(match_list) > 0:
            # Map each update item and it's corresponding field name to a
            # new list so that we can step through it.
            updates_filter = map(None, updates, filter)

            # Step through the match list.
            for line, fpos in match_list:
                # Create a copy of the current record.
                new_record = line.strip().split('|')
                # Step through the updates, applying each one to the new
                # copy of the current record.
                for update, field in updates_filter:
                    # We need to convert it to a string so that we can
                    # store it in our text file.
                    new_record[self.field_names.index(field)] = str(update)

                # Convert the new copy of the current record back into a
                # line appropriate for writing back out to the text file.
                # Run each field through encoder to handle special
                # characters.
                new_line = '|'.join(map(self._encodeString, new_record))
                
                # Since we are changing the current record, we will first
                # write over it with all blank spaces in the file.
                self._deleteRecord(fptr, fpos, line)

                # If the updated copy of the record is not bigger than the
                # old copy, then we can just write it in the same spot in
                # the file.  If it is bigger, then we will have to append
                # it to the end of the file.
                if len(new_line) > len(line):
                    self._writeRecord(fptr, 'end', new_line)
                    # If we didn't overwrite the current record, that means
                    # we have another blank record (i.e. delete record) out
                    # there, so we need to increment the deleted records
                    # counter.
                    self._incrDeleteCounter(fptr)
                else:
                    self._writeRecord(fptr, fpos, new_line)

        # Close the table.
        self._closeTable(fptr)

        # Return the number of records updated.
        return len(match_list)

    #----------------------------------------------------------------------
    # delete
    #----------------------------------------------------------------------
    def delete(self, name, fields, searchData, useRegExp=True):
        """Delete record(s) from table, return number of records deleted.

        Arguments:
            name       - physical file name, including path, that holds
                         table.
            fields     - list containing names of fields to search on. if
                         any of the items in this list is 'recno', then the
                         table will be searched by the recno field only and
                         will delete, at most, one record, since recno is 
                         the system generated primary key.
            searchData - list containing actual data to search on.  Each 
                         item in list corresponds to item in the 'fields'
                         list.

        Returns integer specifying number of records that were deleted.

        Example:
            db.delete('plane.tbl',['country','speed'],['USA','>400'])

            This will search for any plane from the USA with a speed
            greater than 400mph and delete it.
        """
        # If running as a client, then send the command to the server for
        # it to execute.
        if self.connect_type == 'client':
            return self._sendSocket("db.delete('%s',%s,%s,%s)" 
             %(name,fields, searchData, useRegExp))

        # Make copy of searchData list so that value passed in is not 
        # changed if I edit it in validateMatchCriteria.
        patterns = list(searchData)

        # Open the table.
        fptr = self._openTable(name, 'r+')

        # Update the instance variables holding table header info.
        self._updateHeaderVars(fptr)

        try:
            # Check input arguments to make sure they are valid.
            self._validateMatchCriteria(fields, patterns)
        except KBError:
            # If something didn't check out, close the table and re-raise
            # the error.
            fptr.close()
            raise

        # Search the table and populate the match list.
        match_list = self._getMatches(fptr, fields, patterns, useRegExp)

        # If matches were found, delete them.
        if len(match_list) > 0:
            for line, fpos in match_list:
                self._deleteRecord(fptr, fpos, line)
                # Increment the delete counter.
                self._incrDeleteCounter(fptr)

        # Close the table.
        self._closeTable(fptr)

        # Return the number of records deleted.
        return len(match_list)

    #----------------------------------------------------------------------
    # select
    #----------------------------------------------------------------------
    def select(self, name, fields, searchData, filter=None, sortField='',
     ascending=True, useRegExp=True):
        """Select record(s) from table, return list of records selected.

        Arguments:
            name        - physical file name, including path, that holds
                          table.
            fields      - list containing names of fields to search on. If 
                          any of the items in this list is 'recno', then 
                          the table will be searched by the recno field 
                          only and will select, at most, one record, since
                          recno is the system generated primary key.
            searchData  - list containing actual data to search on.  Each
                          item in list corresponds to item in the 'fields'
                          list.
            filter      - list containing names of fields to include for
                          selected records.  If 'filter' list is empty or
                          equal to None, then all fields will be included
                          in result set.
            sortField   - fieldname to sort on.  It must be a valid table
                          field name, and, if filter list is not empty,  
                          the same fieldname must be in the filter list.
            ascending   - Boolean specifying sort direction.

        Returns list of records matching selection criteria.

        Example:
            db.select('plane.tbl',['country','speed'],['USA','>400'])

            This will search for any plane from the USA with a speed
            greater than 400mph and return it.
        """
        # If running as a client, then send the command to the server for
        # it to execute.
        if self.connect_type == 'client':
            return self._sendSocket("db.select('%s',%s,%s,%s,'%s',%s,%s)" 
             %(name, fields, searchData, filter, sortField, ascending, 
             useRegExp))

        # Make copy of searchData list so that value passed in is not 
        # changed if I edit it in validateMatchCriteria.
        patterns = list(searchData)

        # Open the table in read-only mode since we won't be updating it.
        fptr = self._openTable(name, 'r')

        # Update the instance variables holding table header info.
        self._updateHeaderVars(fptr)

        try:
            # Check input arguments to make sure they are valid.
            self._validateMatchCriteria(fields, patterns)
            if filter:
                self._validateFilter(filter)
            else:
                filter = self.field_names
        except KBError:
            # If something didn't check out, close the table and re-raise
            # the error.
            fptr.close()
            raise

        # Validate sort field argument.  It needs to be one of the field
        # names included in the filter.
        if sortField:
            try:
                sortCol = filter.index(sortField)
            except:
                raise KBError('Invalid sort field specified: %s'
                 % sortField)

        # Search table and populate match list.
        match_list = self._getMatches(fptr, fields, patterns, useRegExp)

        # Close the table.
        self._closeTable(fptr)

        # Initialize result set.
        result_set = []
        # Get a list of filter field indexes (i.e., where in the
        # table record is the field that the filter item is
        # referring to.
        filterIndeces = [self.field_names.index(x) for x in filter]

        # For each record in match list, add it to the result set.
        for record, fpos in match_list:
            # Initialize a record to hold the filtered fields of
            # the record.
            result_rec = []

            # Split the record line into it's fields.
            fields = record.split('|')

            # Step through each field index in the filter list. Grab the
            # result field at that position, convert it to
            # proper type, and put it in result set.
            for i in filterIndeces:
                # If the field is empty, don't convert it to its proper
                # type, just append it to the result rec.
                if fields[i] == '':
                    result_rec.append(fields[i])
                # Convert field to its proper type before appending it to
                # the result record.
                elif self.field_types[i] == int:
                    result_rec.append(int(fields[i]))
                elif self.field_types[i] == float:
                    result_rec.append(float(fields[i]))
                # I don't use any methods from the time module here,
                # because the time module won't let you enter any
                # dates before 1970.
                elif self.field_types[i] == datetime.date:
                    # Convert date string to date object and append it.
                    result_rec.append(self._strToDate(fields[i]))
                elif self.field_types[i] == datetime.datetime:
                    # Convert datetime string to datetime object and append
                    # it.
                    result_rec.append(self._strToDateTime(fields[i]))
                elif self.field_types[i] == bool:
                    result_rec.append(bool(fields[i]))    
                else:
                # If field is a string type, we need to run it through
                # the unencoder to translate any special characters
                # back to their original form.
                    result_rec.append(self._unencodeString(fields[i]))

            # Add the result record to the result set.
            result_set.append(result_rec)

        # If a sort field was specified...
        if sortField:
            # Sort result set.  If ascending is FALSE, reverse the two
            # values to sort, so that it will sort descending.
            if ascending:
                result_set.sort( lambda x, y, column=sortCol:
                    cmp(x[column], y[column] ))
            else:
                result_set.sort( lambda x, y, column=sortCol:
                    cmp(y[column], x[column] ))

        # Return the set of records that matched the selection criteria.
        return result_set

    #----------------------------------------------------------------------
    # pack
    #----------------------------------------------------------------------
    def pack(self, name):
        """Remove blank records from table and return total removed.

        Keyword Arguments:
            name - physical file name, including path, that holds table.

        Returns number of blank lines removed from table.
        """
        # If running as a client, then send the command to the server for
        # it to execute.
        if self.connect_type == 'client':
            return self._sendSocket("db.pack('%s')" %(name))

        # Open the table in read-only mode since we won't be updating it.
        fptr = self._openTable(name, 'r')

        # Read in all records.
        lines = fptr.readlines()

        # Close the table so we can re-build it.
        self._closeTable(fptr)

        # Reset number of deleted records to zero.
        header_rec = lines[0].split('|')
        header_rec[1] = "000000"

        # Set first line of re-built file to the header record.
        lines[0] = '|'.join(header_rec)

        # Open the table in write mode since we will be re-building it.
        fptr = self._openTable(name, 'w')

        # This is the counter we will use to report back how many blank
        # records were removed.
        lines_deleted = 0

        # Step through all records in table, only writing out non-blank
        # records.
        for line in lines:
            # By doing a rstrip instead of a strip, we can remove any
            # extra spaces at the end of line that were a result of
            # updating a record with a shorter one.
            line = line.rstrip()
            if line == "":
               lines_deleted += 1
               continue
            try:
                fptr.write(line + '\n')
            except:
                raise KBError('Could not write record in: ' + name)

        # Close the table.
        self._closeTable(fptr)

        # Return number of records removed from table.
        return lines_deleted

    #----------------------------------------------------------------------
    # drop
    #----------------------------------------------------------------------
    def drop(self, name):
        """Delete physical file containing table and return True.

        Arguments:
            name - physical filename, including path, that holds table.

        Returns True if no exceptions are raised.
        """
        # If running as a client, then send the command to the server for
        # it to execute.
        if self.connect_type == 'client':
            return self._sendSocket("db.drop('%s')" %(name))

        # Delete physical file.
        os.remove(name)

        # Return success.
        return True

    #----------------------------------------------------------------------
    # getFieldNames
    #----------------------------------------------------------------------
    def getFieldNames(self, name):
        """Return list of field names for specified table name

        Arguments:
            name - physical file name, including path, that holds table.

        Returns list of field names for table.
        """
        # If running as a client, then send the command to the server for
        # it to execute.
        if self.connect_type == 'client':
            return self._sendSocket("db.getFieldNames('%s')" %(name))

        # Open the table in read-only mode since we won't be updating it.
        fptr = self._openTable(name, 'r')

        # Update the instance variables holding table header info
        self._updateHeaderVars(fptr)

        # Close the table.
        self._closeTable(fptr)

        return self.field_names

    #----------------------------------------------------------------------
    # getFieldTypes
    #----------------------------------------------------------------------
    def getFieldTypes(self, name):
        """Return list of field types for specified table name

        Arguments:
            name - physical file name, including path, that holds table.

        Returns list of field types for table.
        """
        # If running as a client, then send the command to the server for
        # it to execute.
        if self.connect_type == 'client':
            return self._sendSocket("db.getFieldTypes('%s')" %(name))

        # Open the table in read-only mode since we won't be updating it.
        fptr = self._openTable(name, 'r')

        # Update the instance variables holding table header info
        self._updateHeaderVars(fptr)

        # Close the table.
        self._closeTable(fptr)

        return self.field_types


    #----------------------------------------------------------------------
    # len
    #----------------------------------------------------------------------
    def len(self, name):
        '''Return total number of non-deleted records in specified table

        Arguments:
            name - physical file name, including path, that holds table.

        Returns total number of records in table.
        '''
        # If running as a client, then send the command to the server for
        # it to execute.
        if self.connect_type == 'client':
            return self._sendSocket("db.len('%s')" %(name))

        # Initialize counter.
        rec_count = 0

        # Open the table in read-only mode since we won't be updating it.
        fptr = self._openTable(name, 'r')

        # Skip header record.
        line = fptr.readline()

        # Loop through entire table.
        line = fptr.readline()
        while line:
            # Strip off newline character.
            line = line[0:-1]

            # If not blank line, add 1 to record count.
            if line.strip() != "":
                rec_count += 1

            # Read next record.
            line = fptr.readline()

        # Close the table.
        self._closeTable(fptr)

        return rec_count

    #----------------------------------------------------------------------
    # PRIVATE METHODS
    #----------------------------------------------------------------------


    #----------------------------------------------------------------------
    # _strToDate
    #----------------------------------------------------------------------
    def _strToDate(self, dateString):
        # Split the date string up into pieces and create a
        # date object.
        y, m, d = dateString.split('-')
        return datetime.date(int(y), int(m), int(d))
        
    #----------------------------------------------------------------------
    # _strToDateTime
    #----------------------------------------------------------------------
    def _strToDateTime(self, dateTimeString):
        # Split datetime string into datetime portion microseconds portion.
        tempDateTime = dateTimeString.split('.')
        # Were there microseconds in the datetime string.
        if len(tempDateTime) > 1:
            microsec = int(tempDateTime[1])
        else:
            microsec = 0
        # Now, split the datetime portion into a date
        # and a time string.  Take all of the pieces and
        # create a datetime object.
        tempDate, tempTime = tempDateTime[0].split(' ')
        y, m, d = tempDate.split('-')
        h, min, sec = tempTime.split(':')
        return datetime.datetime(int(y),int(m),int(d),int(h),int(min),
         int(sec),microsec)
         
    #----------------------------------------------------------------------
    # _encodeString
    #----------------------------------------------------------------------
    def _encodeString(self, s):
        '''Encode a string.

        Translates problem characters like \n, \r, and \032 to benign
        character strings.

        Keyword Arguments:
            s - string to encode.

        Returns encoded string.
        '''
        if self.encodeRegExp.search(s):
            s = s.replace('\n', '&linefeed;')
            s = s.replace('\r', '&carriage_return;')
            s = s.replace('\032', '&substitute;')
            s = s.replace('|', '&pipe;')
        return s

    #----------------------------------------------------------------------
    # _unencodeString
    #----------------------------------------------------------------------
    def _unencodeString(self, s):
        '''Unencode a string.

        Translates encoded character strings back to special characters
        like \n, \r, \032.

        Keyword Arguments:
            s - string to unencode.

        Returns unencoded string.
        '''
        if self.unencodeRegExp.search(s):
            s = s.replace('&linefeed;', '\n')
            s = s.replace('&carriage_return;', '\r')
            s = s.replace('&substitute;', '\032')
            s = s.replace('&pipe;', '|')
        return s

    #----------------------------------------------------------------------
    # _updateHeaderVars
    #----------------------------------------------------------------------
    def _updateHeaderVars(self, fptr):
        # Go to the header record and read it in.
        fptr.seek(0)
        line = fptr.readline()

        # Chop off the newline character.
        line = line[0:-1]

        # Split the record into fields.
        header_rec = line.split('|')

        # Update Last Record Number and Deleted Records counters.
        self.last_recno = int(header_rec[0])
        self.del_counter = int(header_rec[1])

        # Skip the recno counter, and the delete counter.
        header_fields = header_rec[2:]

        # Create an instance variable holding the field names.
        self.field_names = [item.split(':')[0] for item in header_fields]
        # Create an instance variable holding the field types.
        self.field_types = []
        for item in [x.split(':')[1] for x in header_fields]:
            if item in ['int', 'Integer']:
                self.field_types.append(int)
            elif item in ['float', 'Float']:
                self.field_types.append(float)
            elif item in ['datetime.date', 'Date']:
                self.field_types.append(datetime.date)
            elif item in ['datetime.datetime', 'DateTime']:
                self.field_types.append(datetime.datetime)
            elif item in ['bool', 'Boolean']:
                self.field_types.append(bool)
            else:
                self.field_types.append(str)

    #----------------------------------------------------------------------
    # _validateMatchCriteria
    #----------------------------------------------------------------------
    def _validateMatchCriteria(self, fields, patterns):
        """Run various checks against list of fields and patterns to be
        used as search criteria.  This method is called from all public
        methods that search the database.
        """
        if len(fields) == 0:
            raise KBError('Length of fields list must be greater ' +
             'than zero.')
        if len(fields) != len(patterns):
            raise KBError('Length of fields list and patterns list ' +
             'not the same.')

        # If any of the list of fields to search on do not match a field
        # in the table, raise an error.
        for i, field_pattern in enumerate(map(None, fields, patterns)):
            field, pattern = field_pattern
            
            if not field in self.field_names:
                raise KBError('Invalid field name in fields list: ' +
                 field)

            if field == 'recno':
                if len(fields) > 1:
                    raise KBError('If selecting by recno, no other ' +
                     'selection criteria is allowed')
                if pattern != '*' and not isinstance(pattern, int):
                    raise KBError('Recno argument is not an integer')

    #----------------------------------------------------------------------
    # _validateUpdateCriteria
    #----------------------------------------------------------------------
    def _validateUpdateCriteria(self, updates, filter):
        """Run various checks against list of updates and fields to be
        used as update criteria.  This method is called from all public
        methods that update the database.
        """
        if len(updates) == 0:
            raise KBError('Length of updates list must be greater ' +
             'than zero.')

        if len(updates) != len(filter):
            raise KBError('Length of updates list and filter list ' +
             'not the same.')
        # Since recno is the record's primary key and is system
        # generated, like an autoincrement field, do not allow user
        # to update it.
        if 'recno' in filter:
            raise KBError("Cannot update value of 'recno' field.")
        # Validate filter list.
        self._validateFilter(filter)

        for update, field_name in map(None, updates, filter):
            if update != '':
                if not isinstance(update, self.field_types[
                 self.field_names.index(field_name)]):
                    raise KBError("Invalid update value for %s" %
                     field_name)

    #----------------------------------------------------------------------
    # _validateFilter
    #----------------------------------------------------------------------
    def _validateFilter(self, filter):
        # Each field in the filter list must be a valid field in the table.
        for field in filter:
            if not field in self.field_names:
                raise KBError('Invalid field name: %s' % field)

    #----------------------------------------------------------------------
    # _getMatches
    #----------------------------------------------------------------------
    def _getMatches(self, fptr, fields, patterns, useRegExp):
        # Initialize a list to hold all records that match the search
        # criteria.
        match_list = []

        # If one of the fields to search on is 'recno', which is the
        # table's primary key, then search just on that field and return
        # at most one record.
        if 'recno' in fields:
            match_list = self._getMatchByRecno(fptr,
             patterns[fields.index('recno')])
        # Otherwise, search table, using all search fields and patterns
        # specified in arguments lists.
        else:
            new_patterns = [] 
            
            fieldNrs = [self.field_names.index(x) for x in fields]
            
            for fieldPos, pattern in zip(fieldNrs, patterns):
                if self.field_types[fieldPos] == str:
                    new_patterns.append(pattern)
                elif self.field_types[fieldPos] == bool:
                    # If type is boolean, I am going to coerce it to be
                    # either True or False by applying bool to it.  This
                    # is because it could be '' or [].  Next, I am going
                    # to convert it to the string representation: either
                    # 'True' or 'False'.  The reason I do this is because
                    # that is how it is stored in each record of the table
                    # and it is a lot faster to change this one value from
                    # boolean to string than to change possibly thousands
                    # of table values from string to boolean.  And, if they
                    # both are either 'True' or 'False' and can still
                    # compare them using the equality test and get the same
                    # result as if they were both booleans.
                    new_patterns.append(str(bool(pattern)))
                else:
                    r = re.search('[\s]*[\+-]?\d',pattern)
                    patternComparison = pattern[:r.start()]
                    if self.field_types[fieldPos] == int:
                        patternValue = int(pattern[r.start():])
                    elif self.field_types[fieldPos] == float:
                        patternValue = float(pattern[r.start():])
                    else:
                        patternValue = pattern[r.start():]
                    new_patterns.append([patternComparison,patternValue]) 

            fieldPos_new_patterns = zip(fieldNrs, new_patterns)
            maxfield = max(fieldNrs)+1

            # Record current position in table. Then read first detail
            # record.
            fpos = fptr.tell()
            line = fptr.readline()

            # Loop through entire table.
            while line:
                # Strip off newline character.
                line = line[:-1]
                # Strip off any trailing spaces. 
                line = line.strip()
                try:
                    # If blank line, skip this record.
                    if line == "":
                        raise 'No Match'
                    # Split the line up into fields.
                    record = line.split("|", maxfield)

                    # Foreach correspond field and pattern, check to see
                    # if the table record's field matches successfully.
                    for fieldPos, pattern in fieldPos_new_patterns:
                        # If the field type is string, it
                        # must be a regular expression, so we will
                        # compare the table record's field to it
                        # using the regular expression engine.  Since it is
                        # a string field, we will need to run it through
                        # the unencodeString function to change any special
                        # characters back to their original values.
                        if self.field_types[fieldPos] == str:
                            try:
                                if useRegExp:
                                    if not re.search(pattern,
                                     self._unencodeString(record[fieldPos])
                                     ):
                                        raise 'No Match'
                                else:
                                    if record[fieldPos] != pattern:
                                        raise 'No Match'        
                            except Exception:
                                raise KBError(
                                 'Invalid match expression for %s'
                                 % self.field_names(fieldPos))
                        # If the field type is boolean, then I will simply
                        # do an equality comparison.  See comments above
                        # about why I am actually doing a string compare
                        # here rather than a boolean compare.
                        elif self.field_types[fieldPos] == bool:
                            if not record[fieldPos] == pattern:
                                raise 'No Match'
                        # If it is not a string or a boolean, then it must 
                        # be a number or a date.
                        else:
                            if self.field_types[fieldPos] == int:
                                tableValue = int(record[fieldPos])
                            elif self.field_types[fieldPos] == float:
                                tableValue = float(record[fieldPos])
                            elif self.field_types[fieldPos] in (
                             datetime.date, datetime.datetime):
                                tableValue = record[fieldPos]
                            else:
                                # If it falls through to here, then,
                                # somehow, a bad field type got put into
                                # the table and we show an error.
                                raise KBError('Invalid field type for %s'
                                 % self.field_names(fieldPos))
                            # Now we do the actual comparison.  I used to
                            # just do an eval against the pattern string
                            # here, but I found that eval's are VERY slow.
                            # So, now I determine what type of comparison
                            # they are trying to do and I do it directly.
                            # This sped up queries by 40%.     
                            if pattern[0] == ">=":
                                if not tableValue >= pattern[1]:
                                    raise 'No Match'
                            elif pattern[0] == "<=":
                                if not tableValue <= pattern[1]:
                                    raise 'No Match'
                            elif pattern[0] == "==":
                                if not tableValue == pattern[1]:
                                    raise 'No Match'
                            elif pattern[0] ==  "!=" or pattern[0] == "<>":
                                if not tableValue != pattern[1]:
                                    raise 'No Match'
                            elif pattern[0] == ">":
                                if not tableValue > pattern[1]:
                                    raise 'No Match'
                            elif pattern[0] == "<": 
                                if not tableValue < pattern[1]:
                                    raise 'No Match'
                            else:
                                raise KBError("Invalid comparison operators for: %s %s" % (pattern[0],pattern[1]))
                # If a 'No Match' exception was raised, then go to the
                # next record, otherwise, add it to the list of matches.
                except 'No Match':
                    pass
                else:
                    match_list.append([line, fpos])
                # Save the file position BEFORE we read the next record,
                # because after a read it is pointing at the END of the
                # current record, which, of course, is also the BEGINNING
                # of the next record.  That's why we have to save the
                # position BEFORE we read the next record.
                fpos = fptr.tell()
                line = fptr.readline()

        # After searching, return the list of matched records.
        return match_list

    #----------------------------------------------------------------------
    # _getMatchByRecno
    #----------------------------------------------------------------------
    def _getMatchByRecno(self, fptr, recno):
        # Initialize list of matches.
        match_list = []

        # Initialize table location marker and read in first record
        # of table.
        fpos = fptr.tell()
        line = fptr.readline()

        # Loop through the records of the table.
        while line:
            # Strip of newline character.
            line = line[0:-1]

            # If line is not blank, split it up into fields.
            if line.strip() != "":
                record = line.split("|")
                # If record number for current record equals record number
                # we are searching for, add it to match list and quit
                # searching table.
                if recno == '*' or recno == int(record[0]):
                    match_list.append([line, fpos])
                    if recno != '*':
                        break

            # If we didn't find a match, update the table location marker
            # and read the next record.
            fpos = fptr.tell()
            line = fptr.readline()

        # Return the list of matches.  In this case, will either be empty
        # or will contain only one record.
        return match_list

    #----------------------------------------------------------------------
    # _incrRecnoCounter
    #----------------------------------------------------------------------
    def _incrRecnoCounter(self, fptr):
        # Save where we are in the table.
        last_pos = fptr.tell()

        # Go to header record and grab header fields.
        fptr.seek(0)
        line = fptr.readline()
        header_rec = line[0:-1].split('|')

        # Increment the recno counter.
        self.last_recno += 1
        header_rec[0] = "%06d" %(self.last_recno)

        # Write the header record back to the file.  Run each field through
        # encoder to handle special characters.
        self._writeRecord(fptr, 0, '|'.join(header_rec))

        # Go back to where you were in the table.
        fptr.seek(last_pos)

        return self.last_recno

    #----------------------------------------------------------------------
    # _incrDeleteCounter
    #----------------------------------------------------------------------
    def _incrDeleteCounter(self, fptr):
        # Save where we are in the table.
        last_pos = fptr.tell()

        # Go to header record and grab header fields.
        fptr.seek(0)
        line = fptr.readline()
        header_rec = line[0:-1].split('|')

        # Increment the delete counter.
        self.del_counter += 1
        header_rec[1] = "%06d" %(self.del_counter)

        # Write the header record back to the file.
        self._writeRecord(fptr, 0, '|'.join(header_rec))

        # Go back to where you were in the table.
        fptr.seek(last_pos)

    #----------------------------------------------------------------------
    # _deleteRecord
    #----------------------------------------------------------------------
    def _deleteRecord(self, fptr, pos, record):
        # Move to record position in table.
        fptr.seek(pos)

        # Overwrite record with all spaces.
        self._writeRecord(fptr, pos, " " * len(record))

    #----------------------------------------------------------------------
    # _writeRecord
    #----------------------------------------------------------------------
    def _writeRecord(self, fptr, pos, record):
        try:
            # If record is to be appended, go to end of table and write
            # record, adding newline character.
            if pos == 'end':
                fptr.seek(0, 2)
                fptr.write(record + '\n')
            else:
                # Otherwise, move to record position in table and write
                # record.
                fptr.seek(pos)
                fptr.write(record)
        except:
            raise KBError('Could not write record to: ' + name)

    #----------------------------------------------------------------------
    # _openTable
    #----------------------------------------------------------------------
    def _openTable(self, name, access):
        try:
            # Open physical file holding table.
            fptr = open(name, access)

        except:
            raise KBError('Could not open table: ' + name)
        # Return handle to physical file.
        return fptr

    #----------------------------------------------------------------------
    # _closeTable
    #----------------------------------------------------------------------
    def _closeTable(self, fptr):
        try:
            # Close the file containing the table.
            fptr.close()
        except:
            raise KBError('Could not close table: ' + name)

    #----------------------------------------------------------------------
    # _sendSocket
    #----------------------------------------------------------------------
    def _sendSocket(self, command):
        # Send the method call to the server.
        self.dbSock.sendall(command)

        # Receive the return value of the method.
        recv_length = int(self.dbSock.recv(1024))

        # Keep receiving data until length of data received equals
        # recv_length.
        data = ''

        while len(data) < recv_length:
            data += self.dbSock.recv(recv_length)

        # Convert pickled binary data back into it's original format
        # (usually a list).
        data = cPickle.loads(data)

        # If the server passed back an error object, re-raise that error
        # here on the client side, otherwise, just return the data to the
        # caller.
        if isinstance(data, Exception):
            raise data
        else:
            return data

#--------------------------------------------------------------------------
# KBError Class
#--------------------------------------------------------------------------
class KBError(Exception):
    """Exception class for Database Management System.

    Public Methods:
        __init__ - Create an instance of exception.
    """
    #----------------------------------------------------------------------
    # init
    #----------------------------------------------------------------------
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return `self.value`

    # I overrode repr so I could pass error objects from the server to the
    # client across the network.
    def __repr__(self):
        format = """KBError("%s")"""
        return format % (self.value)
