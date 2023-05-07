import * as React from 'react';
import {
  View,
  Text,
  Image,
  Dimensions,
  StatusBar,
  StyleSheet,
  SafeAreaView,
  Platform,
  Alert,
  Linking,
} from 'react-native';
import NfcProxy from '../../NfcProxy';
import NfcManager, {NfcEvents, NfcTech} from 'react-native-nfc-manager';
import {Button, IconButton} from 'react-native-paper';


function HomeScreen(props) {
  const {navigation} = props;
  const [supported, setSupported] = React.useState(null);
  const [enabled, setEnabled] = React.useState(null);
  const padding = 40;
  const width = Dimensions.get('window').width - 2 * padding;

  React.useEffect(() => {
    async function initNfc() {
      try {
        const success = await NfcProxy.init();
        setSupported(success);
        setEnabled(await NfcProxy.isEnabled());

        if (success) {
          function onBackgroundTag(bgTag) {
            navigation.navigate('TagDetail', {tag: bgTag});
          }

          

          // listen to other background tags after the app launched
          NfcManager.setEventListener(
            NfcEvents.DiscoverBackgroundTag,
            onBackgroundTag,
          );

          // listen to the NFC on/off state on Android device
          if (Platform.OS === 'android') {
            NfcManager.setEventListener(
              NfcEvents.StateChanged,
              ({state} = {}) => {
                NfcManager.cancelTechnologyRequest().catch(() => 0);
                if (state === 'off') {
                  setEnabled(false);
                } else if (state === 'on') {
                  setEnabled(true);
                }
              },
            );
          }

        }
      } catch (ex) {
        console.warn(ex);
        Alert.alert('ERROR', 'fail to init NFC', [{text: 'OK'}]);
      }
    }

    initNfc();
  }, [navigation]);

  function renderNfcButtons() {
    return (
      <View
        style={{
          flex: 2,
          alignItems: 'stretch',
          alignSelf: 'center',
          width,
        }}>
        <Button
          mode="contained"
          onPress={async () => {
            const tag = await NfcProxy.readTag();
            if (tag) {
              navigation.navigate('TagDetail', {tag});
            }
          }}
          style={{marginBottom: 10}}>
          Transaction
        </Button>
      </View>
    );
  }

  function renderNfcNotEnabled() {
    return (
      <View
        style={{
          flex: 2,
          alignItems: 'stretch',
          alignSelf: 'center',
          width,
        }}>
        <Text style={{textAlign: 'center', marginBottom: 10}}>
          Your NFC is not enabled. Please first enable it and hit CHECK AGAIN
          button
        </Text>

        <Button
          mode="contained"
          onPress={() => NfcProxy.goToNfcSetting()}
          style={{marginBottom: 10}}>
          GO TO NFC SETTINGS
        </Button>

        <Button
          mode="outlined"
          onPress={async () => {
            setEnabled(await NfcProxy.isEnabled());
          }}>
          CHECK AGAIN
        </Button>
      </View>
    );
  }

  return (
    <>
      <StatusBar barStyle="dark-content" />
      <SafeAreaView />
      <View style={{flex: 1, padding}}>
        <View
          style={{
            flex: 3,
            justifyContent: 'center',
            alignItems: 'center',
          }}>
          <Image
            source={require('../../../images/LogoText.png')}
            style={{width: 250, height: 250}}
            resizeMode="contain"
          />
        </View>

        {supported && !enabled && renderNfcNotEnabled()}

        {supported && enabled && renderNfcButtons()}
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  settingIcon: {
    position: 'absolute',
    top: Platform.OS === 'android' ? 20 : 0,
    right: 20,
  },
});

export default HomeScreen;
