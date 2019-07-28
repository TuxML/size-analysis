import tuxml
import pandas as pd
import numpy as np

class FeaturesLoader(object):

    def __init__(self, name_csv = 'feature_importanceRF.csv', predict_var ='vmlinux', drop_feature = True, nb_features = 1000):

        self.features = tuxml.load_dataset()
        self.predict_var = predict_var
        self.name_csv = name_csv
        self.nb_features = nb_features
        self.drop_feature = drop_feature

        nb_all_features = 12611
        to_normalize = ['nbyes', 'nbno', 'nbmodule', 'nbyesmodule']
        for feat in to_normalize:
            if feat in self.features.columns:
                self.features[feat] = self.features[feat] / nb_all_features

    def get_features_rf(self):
        df_selection = pd.read_csv(self.name_csv, names=['features', 'imp'], skiprows=0)
        selection = df_selection['features']
        imp = df_selection['imp']
        sorted_imp = sorted(imp, reverse=True)
        threshold_imp = sorted_imp[min(self.nb_features, len(selection)) - 1]
        final = selection[imp > threshold_imp]
        final[len(final)] = self.predict_var
        return final

    def get_features_net(self):
        selection = pd.read_csv(self.name_csv, index_col=0, skiprows=1, names=['feat'])['feat']
        selection[len(selection)] = self.predict_var
        return selection

    def get_features_correlation(self):
        fi_correlation = pd.read_csv(self.name_csv, skiprows=1, names=['features', 'imp'])
        fi_correlation['imp'] = np.abs(fi_correlation['imp'])
        fi_corr = np.array(fi_correlation.sort_values(by='imp', ascending=False)['features'][0:min(len(fi_correlation), self.nb_features)])
        selection = [f for f in fi_corr]
        selection.append(self.predict_var)
        return np.array(selection)

    def get_default(self, drop_features = False):
        selection = pd.read_csv(self.name_csv, names=['features', 'imp'],  skiprows = 1)['features']
        if drop_features:
            selection = selection[0:min(self.nb_features, len(selection))]
        selection[len(selection)] = self.predict_var
        return selection

    def get_features(self):
        if self.name_csv == 'feature_importanceRF.csv':
            return self.get_features_rf()
        if self.name_csv == 'correlations_vmlinux.csv':
            return self.get_features_correlation()
        if self.name_csv == "feature_net.csv":
            return self.get_features_net()
        return self.get_default(drop_features= self.drop_feature)

    def get_selected_features(self):
        return self.features[self.get_features()].replace([2, -1], 0)