import React from 'react';
import { View, Image } from 'react-native';
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';

type LogoProps = {
  height: number;
  width: number;
};

const Logo: React.FC<LogoProps> = ({ height, width }) => {
  return (
    <View className="items-center mb-5">
      <Image
        source={require("../../assets/cropxpertLogo.png")}
        style={{ width: wp(width), height: hp(height) }}
      />
    </View>
  );
};

export default Logo;
