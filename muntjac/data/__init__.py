"""<p>Contains interfaces for the data layer, mainly for binding typed
data and data collections to components, and for validating data.</p>

<h2>Data binding</h2>

<p>The package contains a three-tiered structure for typed data
objects and collections of them:</p>

<ul>
    <li>A {@link com.vaadin.data.Property Property} represents a
    single, typed data value.

    <li>An {@link com.vaadin.data.Item Item} embodies a set of <i>Properties</i>.
    A locally unique (inside the {@link com.vaadin.data.Item Item})
    Property identifier corresponds to each Property inside the Item.</li>
    <li>A {@link com.vaadin.data.Container Container} contains a set
    of Items, each corresponding to a locally unique Item identifier. Note
    that Container imposes a few restrictions on the data stored in it, see
    {@link com.vaadin.data.Container Container} for further information.</li>
</ul>

<p>For more information on the data model, see the <a
    href="http://vaadin.com/book/-/page/datamodel.html">Data model
chapter</a> in Book of Vaadin.</p>

<h2>Buffering</h2>

<p>A {@link com.vaadin.data.Buffered Buffered} implementor is able
to track and buffer changes and commit or discard them later.</p>

<h2>Validation</h2>

<p>{@link com.vaadin.data.Validator Validator} implementations are
used to validate data, typically the value of a {@link
com.vaadin.ui.Field Field}. One or more {@link com.vaadin.data.Validator
Validators} can be added to a {@link com.vaadin.data.Validatable
Validatable} implementor and then used to validate the value of the
Validatable. </p>"""