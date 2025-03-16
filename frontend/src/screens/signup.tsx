import React from "react";
import {
  View,
  Text,
  Image,
  TextInput,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import {
  widthPercentageToDP as wp,
  heightPercentageToDP as hp,
} from "react-native-responsive-screen";
import { FontAwesome, Feather } from "@expo/vector-icons";
import axios from "axios";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../types/naviType";
import { Linking } from "react-native";
import Logo from "../components/Logo";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useState, useContext } from "react";
import { AuthContext } from "../auth/authcontext";
import { baseUrl } from "@env";
import { Picker } from "@react-native-picker/picker";

type Props = NativeStackScreenProps<RootStackParamList, "Signup">;

export default function SignupScreen({ navigation }: Props) {
  const authContext = useContext(AuthContext);

  if (!authContext) {
    return <Text>Loading...</Text>;
  }

  const { setUser } = authContext;
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");

  const handleSignup = async () => {
    const API_URL = `${baseUrl}:5000/auth/signup`;

    console.log("Attempting to sign up...");

    try {
      console.log("Sending data to API:", { email, password, username , role});
      const response = await axios.post(API_URL, {
        email,
        password,
        username,
        role
      });

      console.log("Received response:", response.data.user);

      const { access_token } = response.data;

      if (access_token) {
        console.log("Access token received:", access_token);
        setUser(response.data.user);
        await AsyncStorage.setItem("access_token", access_token);
        navigation.navigate("Home");
      }
    } catch (err) {
      console.error("Error during signup:", err);
      alert("Error while signing up");
    }
  };

  const handleNavigate = async () => {
    console.log("Humaira");
    navigation.navigate("Login");
  };

  const data = [
    { key: "1", value: "Farmer", disabled: true },
    { key: "2", value: "User" },
  ];

  return (
    <View className="bg-white flex flex-1 p-8 justify-evenly  ">
      <Logo height={10} width={20} />

      {/* form section  */}
      <View className="flex-1   justify-evenly">
        <View className="mb-6 items-start">
          <Text className="text-4xl font-semibold text-center">Hi!</Text>
          <Text className="text-center text-gray-500 font-[20px] mt-2">
            Register to to continue
          </Text>
        </View>

        <View className="space-y-4 ">
          <View className="flex-row items-center mb-5  border border-green-400 pl-2 rounded-lg bg-green-100">
            <Picker
              selectedValue={role}
              onValueChange={(itemValue) => setRole(itemValue)}
              style={styles.picker}
            >
              <Picker.Item label="Select a user type" value="" enabled={false} />
              <Picker.Item label="Farmer" value="Farmer" />
              <Picker.Item label="User" value="User" />
            </Picker>
          </View>
          

          <View className="flex-row items-center mb-5 border border-gray-400 pl-2 rounded-lg bg-gray-100">
            <FontAwesome name="user" size={20} color="gray" />
            <TextInput
              placeholder="Username"
              className="flex-1 ml-3"
              value={username}
              onChangeText={setUsername}
            />
          </View>

          <View className="flex-row items-center mb-5 border border-gray-400 pl-2 rounded-lg bg-gray-100">
            <FontAwesome name="user" size={20} color="gray" />
            <TextInput
              placeholder="Email"
              className="flex-1 ml-3"
              value={email}
              onChangeText={setEmail}
            />
          </View>

          <View className="flex-row items-center mb-1 border border-gray-400 pl-2 rounded-lg bg-gray-100">
            <Feather name="lock" size={20} color="gray" />
            <TextInput
              placeholder="Password"
              secureTextEntry
              className="flex-1 ml-3"
              value={password}
              onChangeText={setPassword}
            />
          </View>
          <TouchableOpacity
            className="bg-[#6fca3a] p-3  rounded-lg mt-10 items-center"
            style={{ width: "60%", alignSelf: "center" }}
            onPress={handleSignup}
          >
            <Text className="text-white font-semibold text-2xl">Sign up</Text>
          </TouchableOpacity>
        </View>

        <View className="flex-row items-center my-4">
          <View className="flex-1 h-px bg-gray-500" />
          <Text className="mx-4 text-black text-2xl">or</Text>
          <View className="flex-1 h-px bg-gray-500" />
        </View>

        <TouchableOpacity className="flex-row  p-3 rounded-lg items-center justify-center">
          <Image
            source={require("../../assets/google.png")}
            style={{ width: 28, height: 30, marginRight: 10 }}
          />
          <Text className="text-gray-700">Sign up with Google</Text>
        </TouchableOpacity>

        <View className="mt-5 flex-row justify-center">
          <Text className="text-gray-500">Already have an account? </Text>
          <TouchableOpacity>
            <Text
              className="text-blue-500 font-semibold"
              onPress={handleNavigate}
            >
              Sign in
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20 },
  label: { fontSize: 16, marginBottom: 10 },
  picker: { height: 50, width: "100%" },
});

// import React, { useState, useContext } from "react";
// import { View, Text, Image, TextInput, TouchableOpacity } from "react-native";
// import { FontAwesome, Feather } from "@expo/vector-icons";
// import axios from "axios";
// import { NativeStackScreenProps } from "@react-navigation/native-stack";
// import { RootStackParamList } from "../types/naviType";
// import AsyncStorage from "@react-native-async-storage/async-storage";
// import { AuthContext } from "../auth/authcontext";
// import { baseUrl } from "@env";
// import Logo from "../components/Logo";

// type Props = NativeStackScreenProps<RootStackParamList, "Signup">;

// export default function SignupScreen({ navigation }: Props) {
//   const authContext = useContext(AuthContext);

//   if (!authContext) {
//     return <Text>Loading...</Text>;
//   }

//   const { setUser } = authContext;
//   const [username, setUsername] = useState("");
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [role, setRole] = useState("User");

//   const handleSignup = async () => {
//     const API_URL = `${baseUrl}:5000/auth/signup`;

//     try {
//       const response = await axios.post(API_URL, {
//         email,
//         password,
//         username,
//         role,
//       });

//       const { access_token } = response.data;

//       if (access_token) {
//         setUser(response.data.user);
//         await AsyncStorage.setItem("access_token", access_token);
//         navigation.navigate("Home");
//       }
//     } catch (err) {
//       console.error("Error during signup:", err);
//       alert("Error while signing up");
//     }
//   };

//   return (
//     <View className="bg-white flex flex-1 p-8 justify-evenly">
//       <Logo height={10} width={20} />

//       <View className="flex-1 justify-evenly">
//         <View className="mb-6 items-start">
//           <Text className="text-4xl font-semibold text-center">Hi!</Text>
//           <Text className="text-center text-gray-500 font-[20px] mt-2">
//             Register to continue
//           </Text>
//         </View>

//         <View className="space-y-4">
//           <View className="flex-row items-center mb-5 border border-gray-400 pl-2 rounded-lg bg-gray-100">
//             <FontAwesome name="user" size={20} color="gray" />
//             <TextInput placeholder="Username" className="flex-1 ml-3" value={username} onChangeText={setUsername} />
//           </View>

//           <View className="flex-row items-center mb-5 border border-gray-400 pl-2 rounded-lg bg-gray-100">
//             <FontAwesome name="user" size={20} color="gray" />
//             <TextInput placeholder="Email" className="flex-1 ml-3" value={email} onChangeText={setEmail} />
//           </View>

//           <View className="flex-row items-center mb-1 border border-gray-400 pl-2 rounded-lg bg-gray-100">
//             <Feather name="lock" size={20} color="gray" />
//             <TextInput placeholder="Password" secureTextEntry className="flex-1 ml-3" value={password} onChangeText={setPassword} />
//           </View>

//           {/* Role Selection */}
//           <View className="flex-row justify-between mt-5">
//             <TouchableOpacity
//               className={`p-3 rounded-lg ${role === "Farmer" ? "bg-green-500" : "bg-gray-300"}`}
//               style={{ flex: 1, marginRight: 5 }}
//               onPress={() => setRole("Farmer")}
//             >
//               <Text className="text-white text-center">Farmer</Text>
//             </TouchableOpacity>

//             <TouchableOpacity
//               className={`p-3 rounded-lg ${role === "User" ? "bg-green-500" : "bg-gray-300"}`}
//               style={{ flex: 1, marginLeft: 5 }}
//               onPress={() => setRole("User")}
//             >
//               <Text className="text-white text-center">User</Text>
//             </TouchableOpacity>
//           </View>

//           <TouchableOpacity
//             className="bg-[#6fca3a] p-3 rounded-lg mt-10 items-center"
//             style={{ width: "60%", alignSelf: "center" }}
//             onPress={handleSignup}
//           >
//             <Text className="text-white font-semibold text-2xl">Sign up</Text>
//           </TouchableOpacity>
//         </View>
//       </View>
//     </View>
//   );
// }
