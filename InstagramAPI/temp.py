

def getUserFollowers(self, usernameId, maxid=''):
        if maxid == '':
            return self.SendRequest('friendships/' + str(usernameId) + '/followers/?rank_token=' + self.rank_token)
        else:
            return self.SendRequest('friendships/' + str(usernameId) + '/followers/?rank_token=' + self.rank_token + '&max_id=' + str(maxid))

def getSelfUserFollowers(self):
    return self.getUserFollowers(self.username_id)


def generateUUID(self, type):
        generated_uuid = str(uuid.uuid4())
        if (type):
            return generated_uuid
        else:
            return generated_uuid.replace('-', '')