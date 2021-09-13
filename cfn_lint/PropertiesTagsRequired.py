from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch
import yaml
import os 
import cfnlint


class PropertiesTagsRequired(CloudFormationLintRule):
    """Check if Tags have required keys"""
    id = 'E9000'
    shortdesc = 'Tags have correct key values'
    description = 'Check Tags for resources'
    tags = ['resources', 'tags']

    def __init__ (self,filename):
        
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.folderpath = os.path.join(self.dir_path , 'yaml')
        self.filepath = os.path.join(self.folderpath , filename)
        print(self.filepath)
        self.cfndict = cfnlint.decode.cfn_yaml.load(self.filepath)
        self.cfndict = cfnlint.Template(filename,self.cfndict)
        


    def match(self):
        """Check Tags for required keys"""      

        matches = []
        #print(cfn)
        required_tags = ['CostCenter', 'ApplicationName']
        all_tags = self.cfndict.search_deep_keys('Tags')
        all_tags = [x for x in all_tags if x[0] == 'Resources']
        for all_tag in all_tags:
            all_keys = [d.get('Key') for d in all_tag[-1]]
            for required_tag in required_tags:
                if required_tag not in all_keys:
                    message = "Missing Tag {0} at {1}"
                    matches.append(
                        RuleMatch(
                            all_tag[:-1],
                            message.format(required_tag, '/'.join(map(str, all_tag[:-1])))))

        return matches
        

if __name__ == '__main__':

    app= PropertiesTagsRequired('basic.yaml')
    matches = app.match()
    for match in matches:
        print(match.message)