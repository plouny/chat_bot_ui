
def exec_cond(message, session):
    """ TODO
    Conditions when this exact module is used
    returns: boolean -> True: exec() ; False: pass
    """


def execute(message, session):
    """ TODO
       Execution of giving answer to message
       returns: !!!LIST!!! of messages
       message must be in format:
           {
               "user_id": who will receive this message. If None -> return this message to the author
               "type": "text"/"keyboard"/"image",
               "message": {
                   "content": text_content,
                   "image_id": image_id, # Exist only when type == image
                   "keyboard_buttons": ["option1", "option2", ..], # Exist only when type == keyboard
                   "row_width": row_width  # Exist only when type == keyboard
               }
           }
       """
