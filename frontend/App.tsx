import { StatusBar } from 'expo-status-bar';
import { Text, View } from 'react-native';
import "./global.css"

export default function App() {
  return (
    <View className="bg-blue-500 mt-28 p-4">
      <Text className='text-white'>Open up App.tsx to start working on your app!</Text>
      <StatusBar style="auto" />
    </View>
  );
}
