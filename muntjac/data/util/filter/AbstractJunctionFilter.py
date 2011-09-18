# -*- coding: utf-8 -*-
# from java.util.Arrays import (Arrays,)


class AbstractJunctionFilter(Filter):
    """Abstract base class for filters that are composed of multiple sub-filters.

    The method {@link #appliesToProperty(Object)} is provided to help
    implementing {@link Filter} for in-memory filters.

    @since 6.6
    """
    filters = None

    def __init__(self, *filters):
        self.filters = Collections.unmodifiableCollection(Arrays.asList(filters))

    def getFilters(self):
        """Returns an unmodifiable collection of the sub-filters of this composite
        filter.

        @return
        """
        return self.filters

    def appliesToProperty(self, propertyId):
        """Returns true if a change in the named property may affect the filtering
        result. If some of the sub-filters are not in-memory filters, true is
        returned.

        By default, all sub-filters are iterated to check if any of them applies.
        If there are no sub-filters, false is returned - override in subclasses
        to change this behavior.
        """
        for filter in self.getFilters():
            if filter.appliesToProperty(propertyId):
                return True
        return False


#    @Override
#    public boolean equals(Object obj) {
#        if (obj == null || !getClass().equals(obj.getClass())) {
#            return false;
#        }
#        AbstractJunctionFilter other = (AbstractJunctionFilter) obj;
#        // contents comparison with equals()
#        return Arrays.equals(filters.toArray(), other.filters.toArray());
#    }
#
#    @Override
#    public int hashCode() {
#        int hash = getFilters().size();
#        for (Filter filter : filters) {
#            hash = (hash << 1) ^ filter.hashCode();
#        }
#        return hash;
#    }