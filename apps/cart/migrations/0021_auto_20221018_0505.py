# Generated by Django 3.2.4 on 2022-10-18 09:05

import apps.cart.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0020_alter_shop_data_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_data',
            name='Area_code',
            field=models.CharField(max_length=6, validators=[apps.cart.models.only_int]),
        ),
        migrations.AlterField(
            model_name='shop_data',
            name='Exp_day',
            field=models.CharField(blank=True, choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31')], max_length=2, null=True, validators=[apps.cart.models.only_int]),
        ),
        migrations.AlterField(
            model_name='shop_data',
            name='Exp_month',
            field=models.CharField(blank=True, choices=[('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'), ('05', 'May'), ('06', 'Jun'), ('07', 'July'), ('08', 'August'), ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], max_length=2, null=True, validators=[apps.cart.models.only_int]),
        ),
        migrations.AlterField(
            model_name='shop_data',
            name='Exp_year',
            field=models.CharField(blank=True, choices=[('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030'), ('2031', '2031'), ('2032', '2032'), ('2033', '2033'), ('2034', '2034'), ('2035', '2035'), ('2036', '2036'), ('2037', '2037'), ('2038', '2038'), ('2039', '2039'), ('2040', '2040'), ('2041', '2041'), ('2042', '2042'), ('2043', '2043'), ('2044', '2044'), ('2045', '2045'), ('2046', '2046'), ('2047', '2047'), ('2048', '2048'), ('2049', '2049'), ('2050', '2050'), ('2051', '2051'), ('2052', '2052'), ('2053', '2053'), ('2054', '2054'), ('2055', '2055'), ('2056', '2056'), ('2057', '2057'), ('2058', '2058'), ('2059', '2059'), ('2060', '2060'), ('2061', '2061'), ('2062', '2062'), ('2063', '2063'), ('2064', '2064'), ('2065', '2065'), ('2066', '2066'), ('2067', '2067'), ('2068', '2068'), ('2069', '2069'), ('2070', '2070'), ('2071', '2071'), ('2072', '2072'), ('2073', '2073'), ('2074', '2074'), ('2075', '2075'), ('2076', '2076'), ('2077', '2077'), ('2078', '2078'), ('2079', '2079'), ('2080', '2080'), ('2081', '2081'), ('2082', '2082'), ('2083', '2083'), ('2084', '2084'), ('2085', '2085'), ('2086', '2086'), ('2087', '2087'), ('2088', '2088'), ('2089', '2089'), ('2090', '2090'), ('2091', '2091'), ('2092', '2092'), ('2093', '2093'), ('2094', '2094'), ('2095', '2095'), ('2096', '2096'), ('2097', '2097'), ('2098', '2098'), ('2099', '2099'), ('2100', '2100'), ('2101', '2101'), ('2102', '2102'), ('2103', '2103'), ('2104', '2104'), ('2105', '2105'), ('2106', '2106'), ('2107', '2107'), ('2108', '2108'), ('2109', '2109'), ('2110', '2110'), ('2111', '2111'), ('2112', '2112'), ('2113', '2113'), ('2114', '2114'), ('2115', '2115'), ('2116', '2116'), ('2117', '2117'), ('2118', '2118'), ('2119', '2119'), ('2120', '2120'), ('2121', '2121'), ('2122', '2122'), ('2123', '2123'), ('2124', '2124'), ('2125', '2125'), ('2126', '2126'), ('2127', '2127'), ('2128', '2128'), ('2129', '2129'), ('2130', '2130'), ('2131', '2131'), ('2132', '2132'), ('2133', '2133'), ('2134', '2134'), ('2135', '2135'), ('2136', '2136'), ('2137', '2137'), ('2138', '2138'), ('2139', '2139'), ('2140', '2140'), ('2141', '2141'), ('2142', '2142'), ('2143', '2143'), ('2144', '2144'), ('2145', '2145'), ('2146', '2146'), ('2147', '2147'), ('2148', '2148'), ('2149', '2149'), ('2150', '2150'), ('2151', '2151'), ('2152', '2152'), ('2153', '2153'), ('2154', '2154'), ('2155', '2155'), ('2156', '2156'), ('2157', '2157'), ('2158', '2158'), ('2159', '2159'), ('2160', '2160'), ('2161', '2161'), ('2162', '2162'), ('2163', '2163'), ('2164', '2164'), ('2165', '2165'), ('2166', '2166'), ('2167', '2167'), ('2168', '2168'), ('2169', '2169'), ('2170', '2170'), ('2171', '2171'), ('2172', '2172'), ('2173', '2173'), ('2174', '2174'), ('2175', '2175'), ('2176', '2176'), ('2177', '2177'), ('2178', '2178'), ('2179', '2179'), ('2180', '2180'), ('2181', '2181'), ('2182', '2182'), ('2183', '2183'), ('2184', '2184'), ('2185', '2185'), ('2186', '2186'), ('2187', '2187'), ('2188', '2188'), ('2189', '2189'), ('2190', '2190'), ('2191', '2191'), ('2192', '2192'), ('2193', '2193'), ('2194', '2194'), ('2195', '2195'), ('2196', '2196'), ('2197', '2197'), ('2198', '2198'), ('2199', '2199'), ('2200', '2200'), ('2201', '2201'), ('2202', '2202'), ('2203', '2203'), ('2204', '2204'), ('2205', '2205'), ('2206', '2206'), ('2207', '2207'), ('2208', '2208'), ('2209', '2209'), ('2210', '2210'), ('2211', '2211'), ('2212', '2212'), ('2213', '2213'), ('2214', '2214'), ('2215', '2215'), ('2216', '2216'), ('2217', '2217'), ('2218', '2218'), ('2219', '2219'), ('2220', '2220'), ('2221', '2221'), ('2222', '2222'), ('2223', '2223'), ('2224', '2224'), ('2225', '2225'), ('2226', '2226'), ('2227', '2227'), ('2228', '2228'), ('2229', '2229'), ('2230', '2230'), ('2231', '2231'), ('2232', '2232'), ('2233', '2233'), ('2234', '2234'), ('2235', '2235'), ('2236', '2236'), ('2237', '2237'), ('2238', '2238'), ('2239', '2239'), ('2240', '2240'), ('2241', '2241'), ('2242', '2242'), ('2243', '2243'), ('2244', '2244'), ('2245', '2245'), ('2246', '2246'), ('2247', '2247'), ('2248', '2248'), ('2249', '2249'), ('2250', '2250'), ('2251', '2251'), ('2252', '2252'), ('2253', '2253'), ('2254', '2254'), ('2255', '2255'), ('2256', '2256'), ('2257', '2257'), ('2258', '2258'), ('2259', '2259'), ('2260', '2260'), ('2261', '2261'), ('2262', '2262'), ('2263', '2263'), ('2264', '2264'), ('2265', '2265'), ('2266', '2266'), ('2267', '2267'), ('2268', '2268'), ('2269', '2269'), ('2270', '2270'), ('2271', '2271'), ('2272', '2272'), ('2273', '2273'), ('2274', '2274'), ('2275', '2275'), ('2276', '2276'), ('2277', '2277'), ('2278', '2278'), ('2279', '2279'), ('2280', '2280'), ('2281', '2281'), ('2282', '2282'), ('2283', '2283'), ('2284', '2284'), ('2285', '2285'), ('2286', '2286'), ('2287', '2287'), ('2288', '2288'), ('2289', '2289'), ('2290', '2290'), ('2291', '2291'), ('2292', '2292'), ('2293', '2293'), ('2294', '2294'), ('2295', '2295'), ('2296', '2296'), ('2297', '2297'), ('2298', '2298'), ('2299', '2299'), ('2300', '2300')], max_length=4, null=True, validators=[apps.cart.models.only_int]),
        ),
        migrations.AlterField(
            model_name='shop_data',
            name='Puk_code',
            field=models.CharField(blank=True, max_length=8, null=True, validators=[apps.cart.models.only_int]),
        ),
    ]