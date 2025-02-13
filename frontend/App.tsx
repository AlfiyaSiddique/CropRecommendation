import { Text, View } from 'react-native';
import "./global.css"
import AppNavigation from "./src/navigation/index"

export default function App() {
  return (
    <View className='bg-white flex-1 mt-[40px]'>
      <AppNavigation />
   </View>
  );
}