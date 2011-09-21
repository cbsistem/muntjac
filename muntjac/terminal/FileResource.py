# Copyright (C) 2011 Vaadin Ltd
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from muntjac.service.FileTypeResolver import FileTypeResolver
from muntjac.terminal.ApplicationResource import ApplicationResource
from muntjac.terminal.DownloadStream import DownloadStream
from muntjac.terminal.Terminal import ErrorEvent


class FileResource(ApplicationResource):
    """<code>FileResources</code> are files or directories on local filesystem. The
    files and directories are served through URI:s to the client terminal and
    thus must be registered to an URI context before they can be used. The
    resource is automatically registered to the application when it is created.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

    def __init__(self, sourceFile, application):
        """Creates a new file resource for providing given file for client
        terminals.
        """
        # Default buffer size for this stream resource.
        self._bufferSize = 0
        # File where the downloaded content is fetched from.
        self._sourceFile = None
        # Application.
        self._application = None
        # Default cache time for this stream resource.
        self._cacheTime = DownloadStream.DEFAULT_CACHETIME

        self._application = application
        self.setSourceFile(sourceFile)
        application.addResource(self)


    def getStream(self):
        """Gets the resource as stream.

        @see muntjac.terminal.ApplicationResource#getStream()
        """
        try:
            ds = DownloadStream(file(self._sourceFile),  # FileInputStream
                                self.getMIMEType(),
                                self.getFilename())
            ds.setParameter('Content-Length', str(len(self._sourceFile)))
            ds.setCacheTime(self._cacheTime)
            return ds
        except IOError:
            # Log the exception using the application error handler
            class Error(ErrorEvent):

                def getThrowable(self):
                    return self.e

            self.getApplication().getErrorHandler().terminalError(self.Error())
            return None


    def getSourceFile(self):
        """Gets the source file.

        @return the source File.
        """
        return self._sourceFile


    def setSourceFile(self, sourceFile):
        """Sets the source file.

        @param sourceFile
                   the source file to set.
        """
        self._sourceFile = sourceFile


    def getApplication(self):
        """@see com.vaadin.terminal.ApplicationResource#getApplication()"""
        return self._application


    def getFilename(self):
        """@see com.vaadin.terminal.ApplicationResource#getFilename()"""
        return self._sourceFile.getName()


    def getMIMEType(self):
        """@see com.vaadin.terminal.Resource#getMIMEType()"""
        return FileTypeResolver.getMIMEType(self._sourceFile)


    def getCacheTime(self):
        """Gets the length of cache expiration time. This gives the adapter the
        possibility cache streams sent to the client. The caching may be made in
        adapter or at the client if the client supports caching. Default is
        <code>DownloadStream.DEFAULT_CACHETIME</code>.

        @return Cache time in milliseconds.
        """
        return self._cacheTime


    def setCacheTime(self, cacheTime):
        """Sets the length of cache expiration time. This gives the adapter the
        possibility cache streams sent to the client. The caching may be made in
        adapter or at the client if the client supports caching. Zero or negavive
        value disbales the caching of this stream.

        @param cacheTime
                   the cache time in milliseconds.
        """
        # documented in superclass
        self._cacheTime = cacheTime


    def getBufferSize(self):
        return self._bufferSize


    def setBufferSize(self, bufferSize):
        """Sets the size of the download buffer used for this resource.

        @param bufferSize
                   the size of the buffer in bytes.
        """
        self._bufferSize = bufferSize
