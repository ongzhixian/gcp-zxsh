# User
# Should perform the following operations:
# 1.  Add user
# 2.  Get message
# 3.  Update message
# 4.  Remove message

################################################################################
# Modules and functions import statements
################################################################################

import enum
import logging
from enum import Enum
from queue import Queue
from datetime import datetime
from google.cloud import datastore

from modules.security import sha256_as_hex

################################################################################
# Module variables
################################################################################

db = datastore.Client(namespace="zxsh")
entity_key_queue = Queue()
entity_kind = 'user'

class UserStatus(enum.Enum):
   UnvettedAccount = 0
   VettedAccount = 1

################################################################################
# Define functions
################################################################################

def get_new_entity_key(key_count=10):
    if entity_key_queue.empty():
        try:            
            partial_key = db.key(entity_kind)
            keys = db.allocate_ids(partial_key, key_count)
            for key in keys:
                entity_key_queue.put(key)
        except Exception as e:
            logging.error(e)

    return entity_key_queue.get()

def add_user(email, password):
    logging.info("add_user [{0}], [{1}]".format(email, password))
    password_hash = sha256_as_hex(password)

    try:
        op_datetime = datetime.utcnow()
        logging.info("op_datetime [{0}]".format(op_datetime))

        with db.transaction():
            logging.info("Getting key")
            key = get_new_entity_key()
            logging.info("Key is [{0}]".format(key))
            # parent_key = db.key('zxsh', 'message_list')
            # key = db.key('Task', 'sample_task', parent=parent_key)
            ent = db.get(key)
            logging.info("Entity is [{0}]".format(ent))
            if not ent:
                logging.info("Retrieving entity")
                ent = datastore.Entity(key)
                logging.info("Updating entity")
                ent.update({
                    'body'          : 'sample',
                    'email'         : email,
                    'password_hash' : password,
                    'cre_dt'        : op_datetime,
                    'verify'        : False,
                    'status'        : UserStatus.UnvettedAccount
                })
                logging.info("Putting entity")
                db.put(ent)
                logging.info("All ok returning key")
                return key
                #print("Create loan request: {0}".format(data['nric']))
    except Exception as e:
        logging.error(str(dir(e)))
        logging.error(e)


