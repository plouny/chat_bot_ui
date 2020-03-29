
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
            "type": "text"/"keyboard"/"image",
            "message": {
                "content": text_content/ ["option1", "option2", ..]/image_id,
                "row_width": row_width  # Exist only when type == keyboard
            }
        }
    """
