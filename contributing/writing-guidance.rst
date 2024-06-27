:orphan:

.. _writing-guidance:

Guidance for writing
********************

If you get stuck at all -- please don't hesitate to reach out for help. You
can either leave a comment on this post for general queries, or contact Sally
or one of our admins directly if you need more personal assistance.

General tips and style guide
============================

Documentation consistency in terms of writing style is vital for a good user
experience. In the Server Guide, we use the `Canonical documentation style guide <https://docs.ubuntu.com/styleguide/en>`_.

To make it more straightforward to publish your guide in our documentation, we recommend that you:

- Use a spell checker (set to en-GB).
  
- Be concise and to-the-point in your writing.
  
- Check your links and test your code snippets to make sure they work as expected.

- Link back to other posts on the topic, rather than repeating their content.

- Expand your acronyms the first time they appear on the page, e.g. JavaScript Object Notation (JSON). 
  
- Try not to assume that your reader will have the same knowledge as you. If you're covering a new topic (or something complicated) then try to briefly explain, or link to, things the average reader may not know. 

- If you have used some references you think would be generally helpful to your reader, feel free to include a "Further reading" section at the end of the page. 

Tips and best practices
=======================

- If you're not familiar with Markdown, don't worry! you can always use the style toolbar at the top of the Discourse editing window instead.

- Try not to skip heading levels in your document structure, i.e., a level 2 header (##) should always be followed by a level 3 sub-header (###) not level 4.

- For a numbered list, use ``1.`` in front of each item. The numbering will be
  automatically rendered, so it makes it easier for you to insert new items in
  the list without having to re-number them all:

  .. code-block::

     1. This is the first item

     1. This is the second

     1. This is the third
  

- Unless a list item includes punctuation, don't end it with a full stop. If one item needs a full stop, add one to all the items.

- Enclose a code block with three backticks:

  .. code-block::

     ```text
       ```yaml
       Some code block here
       ```
     ```

- Use separate command input blocks from command output blocks. Avoid using a
  command line prompt (e.g. ``$`` or ``#``) in an input block if possible, and
  precede the output block with some kind of text that explains what's
  happening. For example:
  
  .. code-block::

      ```bash
      uname -r
      ```

      Produces the following output:

      ```text
      4.14.151
      ```

- Use a single backtick to mark inline commands and other string literals, like paths to files.

Feel free to reply to this post if you have any other questions - we will keep it updated with your suggestions and questions!
