import React from 'react';
import {StyleSheet, View, ScrollView, Text} from 'react-native';
import {Button} from 'react-native-paper';
import NdefMessage from '../../Components/NdefMessage';
import {getTechList} from '../../Utils/getTechList';
function TagDetailScreen(props) {
  const {tag} = props.route.params;

  const ndef =
    Array.isArray(tag.ndefMessage) && tag.ndefMessage.length > 0
      ? tag.ndefMessage[0]
      : null;

  return (
    <ScrollView style={[styles.wrapper, {padding: 10}, ]}>

        {ndef ? <NdefMessage ndef={ndef} /> : <Text>---</Text>}
        

    </ScrollView>
  );
}

const styles = StyleSheet.create({
  wrapper: {
    flex: 1,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  section: {
    padding: 8,
    borderRadius: 8,
    backgroundColor: 'white',
    marginBottom: 15,
  },
  sectionLabel: {
    fontSize: 16,
    marginBottom: 5,
    color: 'gray',
  },
});

export default TagDetailScreen;
