   /**
     * 加密<br>
     * 用公钥加密
     *
     * @param data
     * @param key
     * @return
     * @throws Exception
     */
    public static String encryptByPublicKey(byte[] data, String key) throws Exception {
        // 对公钥解密
        byte[] keyBytes = Base64.decodeBase64(key.getBytes(CONTENT_TYPE));

        // 取得公钥
        X509EncodedKeySpec x509KeySpec = new X509EncodedKeySpec(keyBytes);
        KeyFactory keyFactory = KeyFactory.getInstance(KEY_ALGORITHM);
        Key publicKey = keyFactory.generatePublic(x509KeySpec);

        // 对数据加密
        Cipher cipher = Cipher.getInstance(keyFactory.getAlgorithm());
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);
        StringBuffer priString = new StringBuffer();
        byte[] priTemp = new byte[64];
        for (int i = 0, x = 0; i < data.length; i++, x++) {
            if (x == 64) {
                priString.append(bytesToHexStr(cipher.doFinal(priTemp))).append(SEPARATOR);
                x = 0;
                priTemp = new byte[64];
            }
            priTemp[x] = data[i];
            if (i + 1 == data.length) {
                priString.append(bytesToHexStr(cipher.doFinal(priTemp))).append(SEPARATOR);
            }
        }
        return new String(Base64.encodeBase64(priString.toString().getBytes(CONTENT_TYPE)));
    }


     /*
     * 将字符数组转换为16进制字符串
     */
    public static String bytesToHexStr(byte[] bcd) {
        StringBuffer s = new StringBuffer(bcd.length * 2);

        for (int i = 0; i < bcd.length; i++) {
            s.append(bcdLookup[(bcd[i] >>> 4) & 0x0f]);
            s.append(bcdLookup[bcd[i] & 0x0f]);
        }

        return s.toString();
    }